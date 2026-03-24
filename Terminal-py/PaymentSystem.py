import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: PaymentSystem

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def TestStandardFlowsAndZReport():
        d_0_myBank_: BankServer
        nw0_ = BankServer()
        nw0_.ctor__()
        d_0_myBank_ = nw0_
        d_1_pos_: PaymentTerminal
        nw1_ = PaymentTerminal()
        nw1_.ctor__(d_0_myBank_)
        d_1_pos_ = nw1_
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n----------------------------------------------------------\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " SUITE 1: Standard Operations & Z-Report\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " Initial Balances: Card 1111 = $1000 | Card 2222 = $3000\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n----------------------------------------------------------\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n[TEST 1A] Successful Chip Payment: $150 from Card 1111...\n"))).VerbatimString(False))
        (d_1_pos_).StartPayment(150)
        (d_1_pos_).InsertCard(1111)
        if (d_1_pos_.state) == (TerminalState_WaitingForPIN()):
            (d_1_pos_).EnterPin(1234)
            if (d_1_pos_.state) == (TerminalState_Approved()):
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> SUCCESS! Bank authorized $150. New balance: $850.\n"))).VerbatimString(False))
                (d_1_pos_).ClearTerminal()
                (d_1_pos_).RemoveCard()
        if (d_1_pos_.state) == (TerminalState_Idle()):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n[TEST 1B] Successful Chip Payment: $250 from Card 1111...\n"))).VerbatimString(False))
            (d_1_pos_).StartPayment(250)
            (d_1_pos_).InsertCard(1111)
            if (d_1_pos_.state) == (TerminalState_WaitingForPIN()):
                (d_1_pos_).EnterPin(1234)
                if (d_1_pos_.state) == (TerminalState_Approved()):
                    _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> SUCCESS! Bank authorized $250. New balance: $600.\n"))).VerbatimString(False))
                    (d_1_pos_).ClearTerminal()
                    (d_1_pos_).RemoveCard()
        if (d_1_pos_.state) == (TerminalState_Idle()):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n[TEST 1C] Successful Chip Payment: $300 from Card 2222...\n"))).VerbatimString(False))
            (d_1_pos_).StartPayment(300)
            (d_1_pos_).InsertCard(2222)
            if (d_1_pos_.state) == (TerminalState_WaitingForPIN()):
                (d_1_pos_).EnterPin(5678)
                if (d_1_pos_.state) == (TerminalState_Approved()):
                    _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> SUCCESS! Bank authorized $300. New balance: $2700.\n"))).VerbatimString(False))
                    (d_1_pos_).ClearTerminal()
                    (d_1_pos_).RemoveCard()
        if (d_1_pos_.state) == (TerminalState_Idle()):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n[TEST 2] Insufficient Funds Check: $2000 from Card 1111...\n"))).VerbatimString(False))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  (Note: Card 1111 only has $600 left after previous tests)\n"))).VerbatimString(False))
            (d_1_pos_).StartPayment(2000)
            (d_1_pos_).InsertCard(1111)
            if (d_1_pos_.state) == (TerminalState_WaitingForPIN()):
                (d_1_pos_).EnterPin(1234)
                if (d_1_pos_.state) == (TerminalState_Declined()):
                    _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> DECLINED! Bank rejected: Amount ($2000) exceeds current balance.\n"))).VerbatimString(False))
                    (d_1_pos_).ClearTerminal()
                    (d_1_pos_).RemoveCard()
        if (d_1_pos_.state) == (TerminalState_Idle()):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n[TEST 3] User Cancels Transaction Before PIN...\n"))).VerbatimString(False))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  Starting payment of $50 for Card 2222.\n"))).VerbatimString(False))
            (d_1_pos_).StartPayment(50)
            (d_1_pos_).InsertCard(2222)
            if (d_1_pos_.state) == (TerminalState_WaitingForPIN()):
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> Terminal shows 'Enter PIN'. User presses red CANCEL button (X)...\n"))).VerbatimString(False))
                (d_1_pos_).CancelTransaction()
                if (d_1_pos_.state) == (TerminalState_WaitingForCardRemoval()):
                    _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> CANCELLED! Terminal safely aborted. Asking to remove card.\n"))).VerbatimString(False))
                    (d_1_pos_).RemoveCard()
        if (d_1_pos_.state) == (TerminalState_Idle()):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n----------------------------------------------------------\n"))).VerbatimString(False))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " PRINTING END OF DAY Z-REPORT (Local Batch)\n"))).VerbatimString(False))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " Expected: 3 successful transactions (150, 250, 300).\n"))).VerbatimString(False))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n----------------------------------------------------------\n"))).VerbatimString(False))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " Total successful checks: "))).VerbatimString(False))
            _dafny.print(_dafny.string_of(len(d_1_pos_.localBatch)))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n"))).VerbatimString(False))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " Receipts List: "))).VerbatimString(False))
            _dafny.print(_dafny.string_of(d_1_pos_.localBatch))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n"))).VerbatimString(False))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n----------------------------------------------------------\n"))).VerbatimString(False))

    @staticmethod
    def TestContactlessNFC():
        d_0_myBank_: BankServer
        nw0_ = BankServer()
        nw0_.ctor__()
        d_0_myBank_ = nw0_
        d_1_pos_: PaymentTerminal
        nw1_ = PaymentTerminal()
        nw1_.ctor__(d_0_myBank_)
        d_1_pos_ = nw1_
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n----------------------------------------------------------\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " SUITE 2: Contactless Payments (NFC)\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " NFC Limit is set to $500.\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n----------------------------------------------------------\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n[TEST 4] Successful NFC Payment: $150 from Card 1111...\n"))).VerbatimString(False))
        (d_1_pos_).StartPayment(150)
        (d_1_pos_).TapCard(1111)
        if (d_1_pos_.state) == (TerminalState_Approved()):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> SUCCESS! Payment authorized instantly via NFC (No PIN required).\n"))).VerbatimString(False))
            (d_1_pos_).ClearTerminal()
        if (d_1_pos_.state) == (TerminalState_Idle()):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n[TEST 5] NFC Over Limit: $600 from Card 1111...\n"))).VerbatimString(False))
            (d_1_pos_).StartPayment(600)
            (d_1_pos_).TapCard(1111)
            if (d_1_pos_.state) == (TerminalState_Declined()):
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> DECLINED! Amount ($600) exceeds NFC limit ($500). User must INSERT card and enter PIN.\n"))).VerbatimString(False))
                (d_1_pos_).ClearTerminal()
        if (d_1_pos_.state) == (TerminalState_Idle()):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n[TEST 6] NFC Disabled by User/Bank: $150 from Card 2222...\n"))).VerbatimString(False))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  (Note: Card 2222 does not have contactless features enabled in Bank DB)\n"))).VerbatimString(False))
            (d_1_pos_).StartPayment(150)
            (d_1_pos_).TapCard(2222)
            if (d_1_pos_.state) == (TerminalState_Declined()):
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> DECLINED! Bank rejected NFC request. Card chip must be used.\n"))).VerbatimString(False))
                (d_1_pos_).ClearTerminal()

    @staticmethod
    def TestSecurity():
        d_0_myBank_: BankServer
        nw0_ = BankServer()
        nw0_.ctor__()
        d_0_myBank_ = nw0_
        d_1_pos_: PaymentTerminal
        nw1_ = PaymentTerminal()
        nw1_.ctor__(d_0_myBank_)
        d_1_pos_ = nw1_
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n----------------------------------------------------------\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " SUITE 3: Security & Fraud Prevention\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n----------------------------------------------------------\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n[TEST 7] Invalid/Fake Card Inserted (Card 99999)...\n"))).VerbatimString(False))
        (d_1_pos_).StartPayment(100)
        (d_1_pos_).InsertCard(99999)
        if (d_1_pos_.state) == (TerminalState_Declined()):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> DECLINED! Security Alert: Card is not recognized by the Bank DB.\n"))).VerbatimString(False))
            (d_1_pos_).ClearTerminal()
            (d_1_pos_).RemoveCard()
        if (d_1_pos_.state) == (TerminalState_Idle()):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n[TEST 8] Card Blocking Check: 3 Wrong PINs (Card 2222)...\n"))).VerbatimString(False))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  Starting payment of $100. Correct PIN is 5678.\n"))).VerbatimString(False))
            (d_1_pos_).StartPayment(100)
            (d_1_pos_).InsertCard(2222)
            if (d_1_pos_.state) == (TerminalState_WaitingForPIN()):
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> Attempt 1: User enters '0000'.\n"))).VerbatimString(False))
                (d_1_pos_).EnterPin(0)
            if (d_1_pos_.state) == (TerminalState_WaitingForPIN()):
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> Attempt 2: User enters '0000'.\n"))).VerbatimString(False))
                (d_1_pos_).EnterPin(0)
            if (d_1_pos_.state) == (TerminalState_WaitingForPIN()):
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> Attempt 3: User enters '0000'.\n"))).VerbatimString(False))
                (d_1_pos_).EnterPin(0)
            if (d_1_pos_.state) == (TerminalState_Declined()):
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  -> BLOCKED! Maximum PIN attempts (3) reached. Bank permanently blocked Card 2222.\n"))).VerbatimString(False))
                (d_1_pos_).ClearTerminal()
                (d_1_pos_).RemoveCard()

    @staticmethod
    def Main(noArgsParameter__):
        default__.TestStandardFlowsAndZReport()
        default__.TestContactlessNFC()
        default__.TestSecurity()


class TerminalState:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [TerminalState_Idle(), TerminalState_WaitingForCard(), TerminalState_WaitingForPIN(), TerminalState_Approved(), TerminalState_Declined(), TerminalState_WaitingForCardRemoval()]
    @classmethod
    def default(cls, ):
        return lambda: TerminalState_Idle()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_Idle(self) -> bool:
        return isinstance(self, TerminalState_Idle)
    @property
    def is_WaitingForCard(self) -> bool:
        return isinstance(self, TerminalState_WaitingForCard)
    @property
    def is_WaitingForPIN(self) -> bool:
        return isinstance(self, TerminalState_WaitingForPIN)
    @property
    def is_Approved(self) -> bool:
        return isinstance(self, TerminalState_Approved)
    @property
    def is_Declined(self) -> bool:
        return isinstance(self, TerminalState_Declined)
    @property
    def is_WaitingForCardRemoval(self) -> bool:
        return isinstance(self, TerminalState_WaitingForCardRemoval)

class TerminalState_Idle(TerminalState, NamedTuple('Idle', [])):
    def __dafnystr__(self) -> str:
        return f'PaymentSystem.TerminalState.Idle'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, TerminalState_Idle)
    def __hash__(self) -> int:
        return super().__hash__()

class TerminalState_WaitingForCard(TerminalState, NamedTuple('WaitingForCard', [])):
    def __dafnystr__(self) -> str:
        return f'PaymentSystem.TerminalState.WaitingForCard'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, TerminalState_WaitingForCard)
    def __hash__(self) -> int:
        return super().__hash__()

class TerminalState_WaitingForPIN(TerminalState, NamedTuple('WaitingForPIN', [])):
    def __dafnystr__(self) -> str:
        return f'PaymentSystem.TerminalState.WaitingForPIN'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, TerminalState_WaitingForPIN)
    def __hash__(self) -> int:
        return super().__hash__()

class TerminalState_Approved(TerminalState, NamedTuple('Approved', [])):
    def __dafnystr__(self) -> str:
        return f'PaymentSystem.TerminalState.Approved'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, TerminalState_Approved)
    def __hash__(self) -> int:
        return super().__hash__()

class TerminalState_Declined(TerminalState, NamedTuple('Declined', [])):
    def __dafnystr__(self) -> str:
        return f'PaymentSystem.TerminalState.Declined'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, TerminalState_Declined)
    def __hash__(self) -> int:
        return super().__hash__()

class TerminalState_WaitingForCardRemoval(TerminalState, NamedTuple('WaitingForCardRemoval', [])):
    def __dafnystr__(self) -> str:
        return f'PaymentSystem.TerminalState.WaitingForCardRemoval'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, TerminalState_WaitingForCardRemoval)
    def __hash__(self) -> int:
        return super().__hash__()


class CardStatus:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [CardStatus_NoCard(), CardStatus_CardInserted()]
    @classmethod
    def default(cls, ):
        return lambda: CardStatus_NoCard()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_NoCard(self) -> bool:
        return isinstance(self, CardStatus_NoCard)
    @property
    def is_CardInserted(self) -> bool:
        return isinstance(self, CardStatus_CardInserted)

class CardStatus_NoCard(CardStatus, NamedTuple('NoCard', [])):
    def __dafnystr__(self) -> str:
        return f'PaymentSystem.CardStatus.NoCard'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, CardStatus_NoCard)
    def __hash__(self) -> int:
        return super().__hash__()

class CardStatus_CardInserted(CardStatus, NamedTuple('CardInserted', [])):
    def __dafnystr__(self) -> str:
        return f'PaymentSystem.CardStatus.CardInserted'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, CardStatus_CardInserted)
    def __hash__(self) -> int:
        return super().__hash__()


class Transaction:
    @classmethod
    def default(cls, ):
        return lambda: Transaction_TxPayment(int(0), int(0), int(0))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_TxPayment(self) -> bool:
        return isinstance(self, Transaction_TxPayment)

class Transaction_TxPayment(Transaction, NamedTuple('TxPayment', [('receiptId', Any), ('amount', Any), ('merchantId', Any)])):
    def __dafnystr__(self) -> str:
        return f'PaymentSystem.Transaction.TxPayment({_dafny.string_of(self.receiptId)}, {_dafny.string_of(self.amount)}, {_dafny.string_of(self.merchantId)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Transaction_TxPayment) and self.receiptId == __o.receiptId and self.amount == __o.amount and self.merchantId == __o.merchantId
    def __hash__(self) -> int:
        return super().__hash__()


class BankServer:
    def  __init__(self):
        self.bankDB: _dafny.Map = _dafny.Map({})
        self.bankBalances: _dafny.Map = _dafny.Map({})
        self.dailyWithdrawn: _dafny.Map = _dafny.Map({})
        self.history: _dafny.Map = _dafny.Map({})
        self.blockedCards: _dafny.Set = _dafny.Set({})
        self.contactlessEnabled: _dafny.Set = _dafny.Set({})
        self.nextReceiptId: int = int(0)
        pass

    def __dafnystr__(self) -> str:
        return "PaymentSystem.BankServer"
    def Valid(self):
        def lambda0_(forall_var_0_):
            d_0_c_: int = forall_var_0_
            return not ((d_0_c_) in (self.bankDB)) or ((((d_0_c_) in (self.bankBalances)) and ((d_0_c_) in (self.dailyWithdrawn))) and ((d_0_c_) in (self.history)))

        def lambda1_(forall_var_1_):
            d_1_c_: int = forall_var_1_
            return not ((d_1_c_) in (self.dailyWithdrawn)) or (((self.dailyWithdrawn)[d_1_c_]) <= ((self).dailyLimit))

        def lambda2_(forall_var_2_):
            d_2_c_: int = forall_var_2_
            return not ((d_2_c_) in (self.contactlessEnabled)) or ((d_2_c_) in (self.bankDB))

        return ((((((_dafny.quantifier((self.bankDB).keys.Elements, True, lambda0_)) and ((((self).merchantId) in (self.bankBalances)) and (((self).merchantId) in (self.history)))) and (_dafny.quantifier((self.dailyWithdrawn).keys.Elements, True, lambda1_))) and (_dafny.quantifier((self.contactlessEnabled).Elements, True, lambda2_))) and ((1111) in (self.bankDB))) and ((2222) in (self.bankDB))) and ((self.nextReceiptId) > (0))

    def ctor__(self):
        (self).bankDB = _dafny.Map({1111: 1234, 2222: 5678})
        (self).bankBalances = _dafny.Map({1111: 1000, 2222: 3000, (self).merchantId: 0})
        (self).dailyWithdrawn = _dafny.Map({1111: 0, 2222: 0})
        (self).history = _dafny.Map({1111: _dafny.SeqWithoutIsStrInference([]), 2222: _dafny.SeqWithoutIsStrInference([]), (self).merchantId: _dafny.SeqWithoutIsStrInference([])})
        (self).blockedCards = _dafny.Set({})
        (self).contactlessEnabled = _dafny.Set({1111})
        (self).nextReceiptId = 1

    def IsValidCard(self, card):
        return (card) in (self.bankDB)

    def IsContactlessEnabled(self, card):
        return (card) in (self.contactlessEnabled)

    def VerifyPin(self, card, pin):
        return (((card) in (self.bankDB)) and ((card) not in (self.blockedCards))) and (((self.bankDB)[card]) == (pin))

    def IsBlocked(self, card):
        return (card) in (self.blockedCards)

    def BlockCard(self, card):
        (self).blockedCards = (self.blockedCards) | (_dafny.Set({card}))

    def CanAuthorizePayment(self, card, amount):
        return ((((card) in (self.bankDB)) and ((card) not in (self.blockedCards))) and ((amount) <= ((self.bankBalances)[card]))) and ((((self.dailyWithdrawn)[card]) + (amount)) <= ((self).dailyLimit))

    def AuthorizePayment(self, card, amount):
        success: bool = False
        receiptId: int = int(0)
        if (self).CanAuthorizePayment(card, amount):
            receiptId = self.nextReceiptId
            (self).nextReceiptId = (self.nextReceiptId) + (1)
            (self).bankBalances = (self.bankBalances).set(card, ((self.bankBalances)[card]) - (amount))
            (self).bankBalances = (self.bankBalances).set((self).merchantId, ((self.bankBalances)[(self).merchantId]) + (amount))
            (self).dailyWithdrawn = (self.dailyWithdrawn).set(card, ((self.dailyWithdrawn)[card]) + (amount))
            (self).history = (self.history).set(card, ((self.history)[card]) + (_dafny.SeqWithoutIsStrInference([Transaction_TxPayment(receiptId, amount, (self).merchantId)])))
            rhs0_ = True
            rhs1_ = receiptId
            success = rhs0_
            receiptId = rhs1_
            return success, receiptId
        rhs2_ = False
        rhs3_ = 0
        success = rhs2_
        receiptId = rhs3_
        return success, receiptId
        return success, receiptId

    @property
    def merchantId(self):
        return 9999
    @property
    def dailyLimit(self):
        return 5000

class PaymentTerminal:
    def  __init__(self):
        self.state: TerminalState = TerminalState.default()()
        self.cardStatus: CardStatus = CardStatus.default()()
        self.pinAttempts: int = int(0)
        self.currentCard: int = int(0)
        self.currentAmount: int = int(0)
        self.localBatch: _dafny.Seq = _dafny.Seq({})
        self._bank: BankServer = None
        pass

    def __dafnystr__(self) -> str:
        return "PaymentSystem.PaymentTerminal"
    def Valid(self):
        def lambda0_(forall_var_0_):
            def lambda1_(exists_var_0_):
                d_1_c_: int = exists_var_0_
                return ((d_1_c_) in ((self).bank.history)) and ((d_0_tx_) in (((self).bank.history)[d_1_c_]))

            d_0_tx_: Transaction = forall_var_0_
            return not ((d_0_tx_) in (self.localBatch)) or (_dafny.quantifier(((self).bank.history).keys.Elements, False, lambda1_))

        return ((((((((((self).bank).Valid()) and ((self.pinAttempts) <= ((self).maxPinAttempts))) and (not ((self.state) == (TerminalState_WaitingForPIN())) or (((((self.cardStatus) == (CardStatus_CardInserted())) and ((self.pinAttempts) < ((self).maxPinAttempts))) and ((self.currentAmount) > (0))) and ((self.currentCard) > (0))))) and (not ((self.state) == (TerminalState_Approved())) or ((((self.pinAttempts) < ((self).maxPinAttempts)) and ((self.currentAmount) > (0))) and ((self.currentCard) > (0))))) and (not ((self.state) == (TerminalState_Declined())) or (((self.currentAmount) > (0)) and ((self.currentCard) > (0))))) and (not ((self.state) == (TerminalState_WaitingForCard())) or ((((self.cardStatus) == (CardStatus_NoCard())) and ((self.currentAmount) > (0))) and ((self.currentCard) == (0))))) and (not ((self.state) == (TerminalState_WaitingForCardRemoval())) or ((((self.cardStatus) == (CardStatus_CardInserted())) and ((self.currentAmount) == (0))) and ((self.currentCard) > (0))))) and (not ((self.state) == (TerminalState_Idle())) or ((((self.cardStatus) == (CardStatus_NoCard())) and ((self.currentAmount) == (0))) and ((self.currentCard) == (0))))) and (_dafny.quantifier((self.localBatch).UniqueElements, True, lambda0_))

    def ctor__(self, b):
        (self)._bank = b
        (self).state = TerminalState_Idle()
        (self).cardStatus = CardStatus_NoCard()
        (self).pinAttempts = 0
        (self).currentCard = 0
        (self).currentAmount = 0
        (self).localBatch = _dafny.SeqWithoutIsStrInference([])

    def StartPayment(self, amount):
        (self).currentAmount = amount
        (self).state = TerminalState_WaitingForCard()

    def InsertCard(self, cardNumber):
        (self).currentCard = cardNumber
        (self).cardStatus = CardStatus_CardInserted()
        (self).pinAttempts = 0
        if (not(((self).bank).IsValidCard(cardNumber))) or (((self).bank).IsBlocked(cardNumber)):
            (self).state = TerminalState_Declined()
        elif True:
            (self).state = TerminalState_WaitingForPIN()

    def TapCard(self, cardNumber):
        (self).currentCard = cardNumber
        (self).pinAttempts = 0
        if (self.currentAmount) > ((self).contactlessLimit):
            (self).state = TerminalState_Declined()
        elif (not(((self).bank).IsValidCard(cardNumber))) or (((self).bank).IsBlocked(cardNumber)):
            (self).state = TerminalState_Declined()
        elif not(((self).bank).IsContactlessEnabled(cardNumber)):
            (self).state = TerminalState_Declined()
        elif True:
            d_0_success_: bool
            d_1_rId_: int
            out0_: bool
            out1_: int
            out0_, out1_ = ((self).bank).AuthorizePayment(cardNumber, self.currentAmount)
            d_0_success_ = out0_
            d_1_rId_ = out1_
            if d_0_success_:
                (self).state = TerminalState_Approved()
                (self).localBatch = (self.localBatch) + (_dafny.SeqWithoutIsStrInference([Transaction_TxPayment(d_1_rId_, self.currentAmount, ((self).bank).merchantId)]))
            elif True:
                (self).state = TerminalState_Declined()

    def EnterPin(self, pin):
        if ((self).bank).VerifyPin(self.currentCard, pin):
            d_0_success_: bool
            d_1_rId_: int
            out0_: bool
            out1_: int
            out0_, out1_ = ((self).bank).AuthorizePayment(self.currentCard, self.currentAmount)
            d_0_success_ = out0_
            d_1_rId_ = out1_
            if d_0_success_:
                (self).state = TerminalState_Approved()
                (self).pinAttempts = 0
                (self).localBatch = (self.localBatch) + (_dafny.SeqWithoutIsStrInference([Transaction_TxPayment(d_1_rId_, self.currentAmount, ((self).bank).merchantId)]))
            elif True:
                (self).state = TerminalState_Declined()
        elif True:
            (self).pinAttempts = (self.pinAttempts) + (1)
            if (self.pinAttempts) == ((self).maxPinAttempts):
                ((self).bank).BlockCard(self.currentCard)
                (self).state = TerminalState_Declined()

    def ClearTerminal(self):
        (self).currentAmount = 0
        (self).pinAttempts = 0
        if (self.cardStatus) == (CardStatus_CardInserted()):
            (self).state = TerminalState_WaitingForCardRemoval()
        elif True:
            (self).state = TerminalState_Idle()
            (self).currentCard = 0

    def RemoveCard(self):
        (self).state = TerminalState_Idle()
        (self).cardStatus = CardStatus_NoCard()
        (self).currentCard = 0

    def CancelTransaction(self):
        (self).currentAmount = 0
        (self).pinAttempts = 0
        if (self.state) == (TerminalState_WaitingForCard()):
            (self).state = TerminalState_Idle()
            (self).cardStatus = CardStatus_NoCard()
            (self).currentCard = 0
        elif True:
            (self).state = TerminalState_WaitingForCardRemoval()

    @property
    def bank(self):
        return self._bank
    @property
    def maxPinAttempts(self):
        return 3
    @property
    def contactlessLimit(self):
        return 500
