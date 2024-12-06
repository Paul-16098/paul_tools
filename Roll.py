from .I18n import I18n
from .Tools import color

from typing import TypeVar
from random import Random
from enum import Enum
from pathlib import Path
import re
import time


__all__ = ["Roll"]


T = TypeVar("T")


class Roll:
    rollTextStructureSet: set[str] = {
        r"(\d*)(d|D)(\d+)(( +)?((\+|\-)(\d+)))?"
    }

    class RollType(Enum):
        """the type of the roll.
        """
        NONE = 0

        DND = 1
        COC = 2

    class returnType(Enum):
        """return type
        """
        BigNotSuccess = -2
        notSuccess = -1
        NONE = 0
        success = 1
        BigSuccess = 2

    def __rollTextReplace(self, text: str) -> str:
        """a func

        Args:
            text (str): input

        Returns:
            str: output
        """
        _ = True
        match text.lower():
            case "int" | "intelligence":
                text = "智力"
            case "san" | "sanity":
                text = "理智"
            case _:
                _ = False
        text += " " if _ else ""
        return text

    def __init__(self, debug: bool = False, seed: int | float | str | bytes | bytearray = time.time(),  rollType: RollType = RollType.NONE, logSum: bool = True, isLog: bool = True) -> None:
        self.debug = debug
        self.rollType = rollType
        self.logSum = logSum
        self.isLog = isLog
        self.__seed = seed

        self.__i18n_obj = I18n(dirRoot=str(Path(__file__).parent), langJson={
            "en_us": {
                "updata": "2024/5/24 12:56 UTC+8",
                "any": "{}",
                "file_lang": "en_us",
                "paul_tools__Roll__Roll__Exception__rollText_Not_Match_The_Structure": "rollText will not ben {},will ben {}."
            },
            "zh_hk": {
                "updata": "2024/5/24 12:56 UTC+8",
                "any": "{}",
                "file_lang": "zh_hk",
                "paul_tools__Roll__Roll__Exception__rollText_Not_Match_The_Structure": "rollText 不是{}，而是{}。"
            },
        })
        self.__random_obj = Random()
        self.__random_obj.seed(self.__seed)

        if self.debug:
            print("random.seed: ", self.seed)

    @property
    def seed(self) -> int | float | str | bytes | bytearray:
        return self.__seed

    @seed.setter
    def seed(self, seed: int | float | str | bytes | bytearray) -> None:
        self.__seed = seed
        self.__random_obj.seed(seed)

    def RollNum(self, rollText: str | None = None, *, xD: int | None = None, Dy: int | None = None, sumBonus: int = 0, bonus: int = 0, success: int | None = None, whyJudged: str = ""):
        trueRollText: str
        rollTextNotMatchTheStructure = Exception(self.__i18n_obj.locale(
            "paul_tools__Roll__Roll__Exception__rollText_Not_Match_The_Structure", repr(rollText), repr(self.rollTextStructureSet)))

        if rollText == None:
            if Dy != None:
                trueRollText = f"d{Dy}" if xD == None else f"{xD}d{Dy}"
            else:
                match self.rollType:
                    case self.RollType.COC:
                        trueRollText = "1d100"
                    case self.RollType.DND:
                        trueRollText = "1d20"
                    case _:
                        raise rollTextNotMatchTheStructure
        else:
            trueRollText = rollText

        rollData: list[str] | None = None
        userReg = None
        for rollTextStructure in self.rollTextStructureSet:
            if (tmp1 := re.search(rollTextStructure, trueRollText)) == None:
                continue
            userReg = rollTextStructure
            rollData = [tmp1.group(1), tmp1.group(3), tmp1.group(6)]
            break
        if rollData is None:
            raise rollTextNotMatchTheStructure

        if (rollData[0] == ""):
            rollData[0] = "1"
        intRollData: list[int] = []
        if rollData[2] == None:
            rollData[2] = "0"
        for tmp1 in rollData:
            intRollData.append(int(tmp1))

        try:
            xD, Dy = [intRollData[0], intRollData[1]]
            if sumBonus == 0:
                sumBonus = intRollData[2]

        except ValueError as e:
            raise rollTextNotMatchTheStructure
        rollValueList: list[int] = []
        returnValueList: list[dict] = []
        whyJudged = self.__rollTextReplace(whyJudged)

        if self.debug:
            print(f"rollIntData: {xD}d{Dy}")

        if self.isLog:
            print("="*20)
            _ = f" {success=}" if success != None else ""
            print(
                f"Roll:> {whyJudged}({xD}d{Dy} {sumBonus:+}){_}")
            del _

        # 擲骰
        for i in range(xD):
            _i = i+1
            rollValue = self.__random_obj.randint(1, Dy)
            trueRollValue = rollValue+bonus

            ####
            # #tag DEBUG for debug
            # rollValue = 19
            # trueRollValue = rollValue+bonus
            ####

            addMsg: str = ""
            printColor: str = ""
            RollValueClass = self.returnType.NONE
            if self.rollType != self.RollType.NONE:
                if (success != None):
                    if self.rollType == self.RollType.DND:
                        if trueRollValue >= success:
                            addMsg = f" [{whyJudged}成功]"
                            printColor = "GREEN"
                            RollValueClass = self.returnType.success
                        elif trueRollValue < success:
                            addMsg = f" [{whyJudged}失敗]"
                            printColor = "red"
                            RollValueClass = self.returnType.notSuccess
                    elif self.rollType == self.RollType.COC:
                        if trueRollValue < success:
                            addMsg = f" [{whyJudged}成功]"
                            printColor = "GREEN"
                            RollValueClass = self.returnType.success
                        else:
                            addMsg = f" [{whyJudged}失敗]"
                            printColor = "red"
                            RollValueClass = self.returnType.notSuccess
                if self.rollType == self.RollType.DND and Dy == 20:
                    if rollValue == 20:
                        addMsg = f" [{whyJudged}大成功!]"
                        printColor = "LIGHTGREEN_EX"
                        RollValueClass = self.returnType.BigSuccess
                    elif rollValue == 1:
                        addMsg = f" [{whyJudged}大失敗!]"
                        printColor = "LIGHTRED_EX"
                        RollValueClass = self.returnType.BigNotSuccess
                if self.rollType == self.RollType.COC and Dy == 100:
                    if rollValue == 0:
                        addMsg = f" [{whyJudged}大成功!]"
                        printColor = "LIGHTGREEN_EX"
                        RollValueClass = self.returnType.BigSuccess
                    elif rollValue == 100:
                        addMsg = f" [{whyJudged}大失敗!]"
                        printColor = "LIGHTRED_EX"
                        RollValueClass = self.returnType.BigNotSuccess
            msg: str | None = None
            if self.isLog:
                msgBonus = ""
                if bonus != 0:
                    msgBonus: str = str(bonus)
                    if (msgBonus[0] != "-"):
                        msgBonus = "+" + msgBonus
                    msgBonus += f" = {trueRollValue}"

                msg = f"   {xD}d{Dy}:[{_i:>{len(str(xD))}}] = {rollValue:>0{len(str(Dy))}} {
                    msgBonus}{addMsg}"

                print(*color(msg, color=printColor))

            returnValueList.append({
                "Value": trueRollValue,
                "msg": msg,
                "RollValueClass": RollValueClass
            })
            rollValueList.append(trueRollValue)
            if self.debug:
                print(("rollValueList: ", rollValueList))

        if self.isLog:
            _ = sum(rollValueList)
            msgSumBonus = ""
            if sumBonus != 0:
                msgSumBonus = str(sumBonus)
                if (msgSumBonus[0] != "-"):
                    msgSumBonus = "+" + msgSumBonus
                msgSumBonus = " "+msgSumBonus
                msgSumBonus += f" = {_+sumBonus}"
            if self.logSum:
                print(f"sum = {_}{msgSumBonus}")
            print(f"X̄ = {_/len(rollValueList):.2f}")
            print("="*20)

        return {
            "rollValueList": rollValueList,
            "Type": self.rollType,
            "returnValueList": returnValueList,
            "userReg": userReg,
        }

    def RollList(self,  rollList: list[T], *,   whyJudged: str = "") -> T:
        r: T = self.__random_obj.choice(rollList)
        if self.debug:
            print("rollValue: ", r)
        if self.isLog:
            print("="*20)
            print(f"Roll List:> {whyJudged}({" ".join(map(str, rollList))})")
            print(f"    r={r}")
            print("="*20)
        return r

    def getExpectedValue(self, values: list[int | float], probabilities: list[float]):
        """計算給定值和對應概率的期望值。

        Args:
            values (list[int  |  float]): 一個包含數值的列表。
            probabilities (list[float]): 對應於數值的概率列表。

        Raises:
            ValueError: 如果 values 與 probabilities 長度不等。
            ValueError: 如果概率之和不等於 1。

        Returns:
            float: 計算出的期望值。
        """
        # 導入 numpy 模塊
        import numpy as np
        # 檢查 values 和 probabilities 的長度是否相等
        if len(values) != len(probabilities):
            raise ValueError(f"values 與 probabilities 長度不等。")
        np_values = np.array(values)
        np_probabilities = np.array(probabilities)
        # 確保概率之和為 1
        if np.isclose(np_probabilities.sum(), 1):
            # 計算期望值
            expected_value = np.sum(np_values * np_probabilities)
            return float(expected_value)
        else:
            raise ValueError(f"概率之和並不等於 1，請檢查概率分配。")
