module PaymentSystem {

  // Стани, в яких може перебувати платіжний термінал
  datatype TerminalState = Idle | WaitingForCard | WaitingForPIN | Approved | Declined | WaitingForCardRemoval

  // Фізичний стан карткоприймача (є там картка чи немає)
  datatype CardStatus = NoCard | CardInserted

  // Транзакція: зберігає номер чека (receiptId), суму і ID магазину (merchantId)
  datatype Transaction = TxPayment(receiptId: nat, amount: nat, merchantId: nat)

  // ==========================================
  // BANK SERVER
  // Моделює базу даних банку та логіку авторизації платежів.
  // ==========================================
  class BankServer {
    // nat - це натуральні числа
    const dailyLimit: nat := 5000
    const merchantId: nat := 9999 // Унікальний ID магазину

    // Змінні стану банку (бази даних), словники
    var bankDB: map<nat, nat>                  // Номер картки -> PIN-код
    var bankBalances: map<nat, nat>            // Номер картки -> Баланс
    var dailyWithdrawn: map<nat, nat>          // Номер картки -> Скільки витрачено за день
    var history: map<nat, seq<Transaction>>    // Номер картки -> Історія транзакцій (seq - список)
    var blockedCards: set<nat>                 // Множина заблокованих карток
    var contactlessEnabled: set<nat>           // Множина карток, яким дозволено NFC (безконтакт)
    var nextReceiptId: nat                     // Лічильник для генерації унікальних receiptId

    // ІНВАРІАНТ БАНКУ
    predicate Valid() reads this {
      (forall c :: c in bankDB ==> c in bankBalances && c in dailyWithdrawn && c in history) &&
      (merchantId in bankBalances && merchantId in history) &&
      (forall c :: c in dailyWithdrawn ==> dailyWithdrawn[c] <= dailyLimit) &&
      (forall c :: c in contactlessEnabled ==> c in bankDB) &&
      1111 in bankDB && 2222 in bankDB &&
      nextReceiptId > 0 // Гарантуємо, що номери чеків починаються хоча б з 1
    }

    // КОНСТРУКТОР: ініціалізує початковий стан.
    constructor() ensures Valid() {
      bankDB := map[1111 := 1234, 2222 := 5678];
      bankBalances := map[1111 := 1000, 2222 := 3000, merchantId := 0];
      dailyWithdrawn := map[1111 := 0, 2222 := 0];
      history := map[1111 := [], 2222 := [], merchantId := []];
      blockedCards := {};
      contactlessEnabled := {1111};
      nextReceiptId := 1; // Перший чек матиме номер 1
    }

    predicate IsValidCard(card: nat) reads this { card in bankDB }
    predicate IsContactlessEnabled(card: nat) reads this { card in contactlessEnabled }
    predicate VerifyPin(card: nat, pin: nat) reads this { card in bankDB && card !in blockedCards && bankDB[card] == pin }
    predicate IsBlocked(card: nat) reads this { card in blockedCards }

    method BlockCard(card: nat)
      requires Valid() modifies this
      ensures Valid() && card in blockedCards
      ensures history == old(history)
      ensures nextReceiptId == old(nextReceiptId) // Лічильник не змінюється при блокуванні
    {
      blockedCards := blockedCards + {card};
    }

    predicate CanAuthorizePayment(card: nat, amount: nat)
      requires Valid()
      requires amount > 0
      reads this
    {
      card in bankDB && card !in blockedCards &&
      amount <= bankBalances[card] &&
      dailyWithdrawn[card] + amount <= dailyLimit
    }

    method AuthorizePayment(card: nat, amount: nat) returns (success: bool, receiptId: nat)
      requires Valid()
      requires amount > 0
      modifies this
      ensures Valid()
      ensures success <==> old(CanAuthorizePayment(card, amount))

      // Гарантії для термінала, щоб він міг довести свою узгодженість (Consistency)
      ensures forall c :: c in old(history) ==> c in history
      ensures forall c :: c in old(history) ==> forall tx :: tx in old(history)[c] ==> tx in history[c]

      // Гарантії для генерації чеків:
      ensures success ==> receiptId == old(nextReceiptId)
      ensures success ==> nextReceiptId == old(nextReceiptId) + 1
      ensures !success ==> nextReceiptId == old(nextReceiptId)
      ensures success ==> TxPayment(receiptId, amount, merchantId) in history[card]
    {
      if CanAuthorizePayment(card, amount)
      {
        receiptId := nextReceiptId;
        nextReceiptId := nextReceiptId + 1;

        bankBalances := bankBalances[card := bankBalances[card] - amount];
        bankBalances := bankBalances[merchantId := bankBalances[merchantId] + amount];
        dailyWithdrawn := dailyWithdrawn[card := dailyWithdrawn[card] + amount];
        history := history[card := history[card] + [TxPayment(receiptId, amount, merchantId)]];

        return true, receiptId;
      }
      return false, 0; // 0 як пустий чек при відмові
    }
  }

  // ==========================================
  // PAYMENT TERMINAL
  // ==========================================
  class PaymentTerminal {
    const maxPinAttempts: nat := 3
    const contactlessLimit: nat := 500
    const bank: BankServer

    var state: TerminalState
    var cardStatus: CardStatus
    var pinAttempts: nat
    var currentCard: nat
    var currentAmount: nat
    var localBatch: seq<Transaction>

    predicate Valid() reads this, bank {
      bank.Valid() &&
      pinAttempts <= maxPinAttempts &&
      (state == WaitingForPIN ==> cardStatus == CardInserted && pinAttempts < maxPinAttempts && currentAmount > 0 && currentCard > 0) &&
      (state == Approved ==> pinAttempts < maxPinAttempts && currentAmount > 0 && currentCard > 0) &&
      (state == Declined ==> currentAmount > 0 && currentCard > 0) &&
      (state == WaitingForCard ==> cardStatus == NoCard && currentAmount > 0 && currentCard == 0) &&
      (state == WaitingForCardRemoval ==> cardStatus == CardInserted && currentAmount == 0 && currentCard > 0) &&
      (state == Idle ==> cardStatus == NoCard && currentAmount == 0 && currentCard == 0) &&

      // ІНВАРІАНТ УЗГОДЖЕНОСТІ
      (forall tx :: tx in localBatch ==> exists c :: c in bank.history && tx in bank.history[c])
    }

    constructor(b: BankServer)
      requires b.Valid()
      ensures Valid() && bank == b && state == Idle
    {
      bank := b;
      state := Idle;
      cardStatus := NoCard;
      pinAttempts := 0;
      currentCard := 0;
      currentAmount := 0;
      localBatch := [];
    }

    method StartPayment(amount: nat)
      requires Valid() && state == Idle
      requires amount > 0
      modifies this
      ensures Valid() && state == WaitingForCard && currentAmount == amount
      ensures localBatch == old(localBatch)
    {
      currentAmount := amount;
      state := WaitingForCard;
    }

    method InsertCard(cardNumber: nat)
      requires Valid() && state == WaitingForCard && cardNumber > 0
      modifies this
      ensures Valid() && cardStatus == CardInserted
      ensures !bank.IsValidCard(cardNumber) || bank.IsBlocked(cardNumber) ==> state == Declined && cardStatus == CardInserted
      ensures bank.IsValidCard(cardNumber) && !bank.IsBlocked(cardNumber) ==> state == WaitingForPIN && cardStatus == CardInserted
      ensures localBatch == old(localBatch)
    {
      currentCard := cardNumber;
      cardStatus := CardInserted;
      pinAttempts := 0;

      if !bank.IsValidCard(cardNumber) || bank.IsBlocked(cardNumber) {
        state := Declined;
      } else {
        state := WaitingForPIN;
      }
    }

    method TapCard(cardNumber: nat)
      requires Valid() && state == WaitingForCard && cardNumber > 0
      modifies this, bank
      ensures Valid() && cardStatus == NoCard
      // exists rId, оскільки термінал до виклику банку не знає номер чека
      ensures state == Approved ==> exists rId :: localBatch == old(localBatch) + [TxPayment(rId, old(currentAmount), bank.merchantId)]
      ensures state != Approved ==> localBatch == old(localBatch)
    {
      currentCard := cardNumber;
      pinAttempts := 0;

      if currentAmount > contactlessLimit {
        state := Declined;
      } else if !bank.IsValidCard(cardNumber) || bank.IsBlocked(cardNumber) {
        state := Declined;
      } else if !bank.IsContactlessEnabled(cardNumber) {
        state := Declined;
      } else {
        var success, rId := bank.AuthorizePayment(cardNumber, currentAmount);
        if success {
          state := Approved;
          localBatch := localBatch + [TxPayment(rId, currentAmount, bank.merchantId)];
        } else {
          state := Declined;
        }
      }
    }

    method EnterPin(pin: nat)
      requires Valid() && state == WaitingForPIN
      modifies this, bank
      ensures Valid() && cardStatus == CardInserted
      ensures state == Approved ==> exists rId :: localBatch == old(localBatch) + [TxPayment(rId, old(currentAmount), bank.merchantId)]
      ensures state != Approved ==> localBatch == old(localBatch)
    {
      if bank.VerifyPin(currentCard, pin) {
        var success, rId := bank.AuthorizePayment(currentCard, currentAmount);
        if success {
          state := Approved;
          pinAttempts := 0;
          localBatch := localBatch + [TxPayment(rId, currentAmount, bank.merchantId)];
        } else {
          state := Declined;
        }
      } else {
        pinAttempts := pinAttempts + 1;
        if pinAttempts == maxPinAttempts {
          bank.BlockCard(currentCard);
          state := Declined;
        }
      }
    }

    method ClearTerminal()
      requires Valid() && (state == Approved || state == Declined)
      modifies this
      ensures Valid()
      ensures old(cardStatus) == CardInserted ==> state == WaitingForCardRemoval && cardStatus == CardInserted
      ensures old(cardStatus) == NoCard ==> state == Idle && cardStatus == NoCard
      ensures localBatch == old(localBatch)
    {
      currentAmount := 0;
      pinAttempts := 0;

      if cardStatus == CardInserted {
        state := WaitingForCardRemoval;
      } else {
        state := Idle;
        currentCard := 0;
      }
    }

    method RemoveCard()
      requires Valid() && state == WaitingForCardRemoval
      modifies this
      ensures Valid() && state == Idle && cardStatus == NoCard
      ensures localBatch == old(localBatch)
    {
      state := Idle;
      cardStatus := NoCard;
      currentCard := 0;
    }

    method CancelTransaction()
      requires Valid() && (state == WaitingForCard || state == WaitingForPIN)
      modifies this
      ensures Valid()
      ensures localBatch == old(localBatch)
    {
      currentAmount := 0;
      pinAttempts := 0;
      if state == WaitingForCard {
        state := Idle;
        cardStatus := NoCard;
        currentCard := 0;
      } else {
        state := WaitingForCardRemoval;
      }
    }
  }


  // ТЕСТИ

  // --- Стандартні операції (Чип, Відмова, Скасування + Z-Звіт) ---
  method TestStandardFlowsAndZReport() {
    var myBank := new BankServer();
    var pos := new PaymentTerminal(myBank);

    print "\n----------------------------------------------------------\n";
    print " SUITE 1: Standard Operations & Z-Report\n";
    print " Initial Balances: Card 1111 = $1000 | Card 2222 = $3000\n";
    print "\n----------------------------------------------------------\n";

    print "\n[TEST 1A] Successful Chip Payment: $150 from Card 1111...\n";
    pos.StartPayment(150);
    pos.InsertCard(1111);
    if pos.state == WaitingForPIN {
      pos.EnterPin(1234);
      if pos.state == Approved {
        print "  -> SUCCESS! Bank authorized $150. New balance: $850.\n";
        pos.ClearTerminal();
        pos.RemoveCard();
      }
    }

    if pos.state == Idle {
      print "\n[TEST 1B] Successful Chip Payment: $250 from Card 1111...\n";
      pos.StartPayment(250);
      pos.InsertCard(1111);
      if pos.state == WaitingForPIN {
        pos.EnterPin(1234);
        if pos.state == Approved {
          print "  -> SUCCESS! Bank authorized $250. New balance: $600.\n";
          pos.ClearTerminal();
          pos.RemoveCard();
        }
      }
    }

    if pos.state == Idle {
      print "\n[TEST 1C] Successful Chip Payment: $300 from Card 2222...\n";
      pos.StartPayment(300);
      pos.InsertCard(2222);
      if pos.state == WaitingForPIN {
        pos.EnterPin(5678);
        if pos.state == Approved {
          print "  -> SUCCESS! Bank authorized $300. New balance: $2700.\n";
          pos.ClearTerminal();
          pos.RemoveCard();
        }
      }
    }

    if pos.state == Idle {
      print "\n[TEST 2] Insufficient Funds Check: $2000 from Card 1111...\n";
      print "  (Note: Card 1111 only has $600 left after previous tests)\n";
      pos.StartPayment(2000);
      pos.InsertCard(1111);
      if pos.state == WaitingForPIN {
        pos.EnterPin(1234);
        if pos.state == Declined {
          print "  -> DECLINED! Bank rejected: Amount ($2000) exceeds current balance.\n";
          pos.ClearTerminal();
          pos.RemoveCard();
        }
      }
    }

    if pos.state == Idle {
      print "\n[TEST 3] User Cancels Transaction Before PIN...\n";
      print "  Starting payment of $50 for Card 2222.\n";
      pos.StartPayment(50);
      pos.InsertCard(2222);
      if pos.state == WaitingForPIN {
        print "  -> Terminal shows 'Enter PIN'. User presses red CANCEL button (X)...\n";
        pos.CancelTransaction();
        if pos.state == WaitingForCardRemoval {
          print "  -> CANCELLED! Terminal safely aborted. Asking to remove card.\n";
          pos.RemoveCard();
        }
      }
    }

    if pos.state == Idle {
      print "\n----------------------------------------------------------\n";
      print " PRINTING END OF DAY Z-REPORT (Local Batch)\n";
      print " Expected: 3 successful transactions (150, 250, 300).\n";
      print "\n----------------------------------------------------------\n";
      print " Total successful checks: ", |pos.localBatch|, "\n";
      print " Receipts List: ", pos.localBatch, "\n";
      print "\n----------------------------------------------------------\n";
    }
  }

  method TestContactlessNFC() {
    var myBank := new BankServer();
    var pos := new PaymentTerminal(myBank);

    print "\n----------------------------------------------------------\n";
    print " SUITE 2: Contactless Payments (NFC)\n";
    print " NFC Limit is set to $500.\n";
    print "\n----------------------------------------------------------\n";

    print "\n[TEST 4] Successful NFC Payment: $150 from Card 1111...\n";
    pos.StartPayment(150);
    pos.TapCard(1111);
    if pos.state == Approved {
      print "  -> SUCCESS! Payment authorized instantly via NFC (No PIN required).\n";
      pos.ClearTerminal();
    }

    if pos.state == Idle {
      print "\n[TEST 5] NFC Over Limit: $600 from Card 1111...\n";
      pos.StartPayment(600);
      pos.TapCard(1111);
      if pos.state == Declined {
        print "  -> DECLINED! Amount ($600) exceeds NFC limit ($500). User must INSERT card and enter PIN.\n";
        pos.ClearTerminal();
      }
    }

    if pos.state == Idle {
      print "\n[TEST 6] NFC Disabled by User/Bank: $150 from Card 2222...\n";
      print "  (Note: Card 2222 does not have contactless features enabled in Bank DB)\n";
      pos.StartPayment(150);
      pos.TapCard(2222);
      if pos.state == Declined {
        print "  -> DECLINED! Bank rejected NFC request. Card chip must be used.\n";
        pos.ClearTerminal();
      }
    }
  }

  method TestSecurity() {
    var myBank := new BankServer();
    var pos := new PaymentTerminal(myBank);

    print "\n----------------------------------------------------------\n";
    print " SUITE 3: Security & Fraud Prevention\n";
    print "\n----------------------------------------------------------\n";

    print "\n[TEST 7] Invalid/Fake Card Inserted (Card 99999)...\n";
    pos.StartPayment(100);
    pos.InsertCard(99999);
    if pos.state == Declined {
      print "  -> DECLINED! Security Alert: Card is not recognized by the Bank DB.\n";
      pos.ClearTerminal();
      pos.RemoveCard();
    }

    if pos.state == Idle {
      print "\n[TEST 8] Card Blocking Check: 3 Wrong PINs (Card 2222)...\n";
      print "  Starting payment of $100. Correct PIN is 5678.\n";
      pos.StartPayment(100);
      pos.InsertCard(2222);

      if pos.state == WaitingForPIN {
        print "  -> Attempt 1: User enters '0000'.\n";
        pos.EnterPin(0000);
      }
      if pos.state == WaitingForPIN {
        print "  -> Attempt 2: User enters '0000'.\n";
        pos.EnterPin(0000);
      }
      if pos.state == WaitingForPIN {
        print "  -> Attempt 3: User enters '0000'.\n";
        pos.EnterPin(0000);
      }

      if pos.state == Declined {
        print "  -> BLOCKED! Maximum PIN attempts (3) reached. Bank permanently blocked Card 2222.\n";
        pos.ClearTerminal();
        pos.RemoveCard();
      }
    }
  }

  method Main() {
    TestStandardFlowsAndZReport();
    TestContactlessNFC();
    TestSecurity();
  }
}