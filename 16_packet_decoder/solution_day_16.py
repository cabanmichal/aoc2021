"""https://adventofcode.com/2021/day/16"""

import math
import operator
from abc import ABC, abstractmethod
from typing import Tuple, List


class Packet(ABC):
    def __init__(self, version: int, type_id: int, bits: str) -> None:
        self.version = version
        self.type_id = type_id
        self.bits = bits
        self.children: List["Packet"] = []
        self.length: int = 0

    @abstractmethod
    def make_children(self) -> None:
        """Create child Packets."""

    def version_sum(self) -> int:
        """Solution to part 1."""
        total = self.version
        for child in self.children:
            total += child.version_sum()

        return total

    def get_value(self) -> int:
        """Solution to part 2."""
        if not self.children:
            raise ValueError("Cannot compute value without children.")

        child_values = (c.get_value() for c in self.children)
        if self.type_id == 0:
            value = sum(child_values)
        elif self.type_id == 1:
            value = math.prod(child_values)
        elif self.type_id == 2:
            value = min(child_values)
        elif self.type_id == 3:
            value = max(child_values)
        elif self.type_id == 5:
            value = int(operator.gt(*child_values))
        elif self.type_id == 6:
            value = int(operator.lt(*child_values))
        elif self.type_id == 7:
            value = int(operator.eq(*child_values))
        else:
            raise ValueError(f"Unknown type id: {self.type_id}")

        return value


class LiteralPacket(Packet):
    def __init__(self, version: int, type_id: int, bits: str) -> None:
        super().__init__(version, type_id, bits)
        self.length, self._value = self._parse_data()

    def _parse_data(self) -> Tuple[int, int]:
        bit_groups = []
        for i in range(6, len(self.bits), 5):
            group = self.bits[i : i + 5]
            bit_groups.append(group[1:])
            if group[0] == "0":
                break

        bit_string = "".join(bit_groups)
        length = 6 + len(bit_string) + len(bit_groups)
        value = int(bit_string, 2)

        return length, value

    def make_children(self) -> None:
        pass

    def get_value(self) -> int:
        return self._value


class OperatorPacket(Packet):
    def __init__(
        self, version: int, type_id: int, bits: str, type_bits_count: int
    ) -> None:
        super().__init__(version, type_id, bits)
        self.header_length = 6 + 1 + type_bits_count
        self.length = self.header_length
        self.children_stop_value = int(self.bits[6 + 1 : self.header_length], 2)

    @abstractmethod
    def should_make_more_children(self) -> bool:
        ...

    def make_children(self) -> None:
        while self.should_make_more_children():
            data = self.bits[self.length :]
            child = packet_factory(data)
            child.make_children()
            self.children.append(child)
            self.length += child.length


class OperatorPacket0(OperatorPacket):
    def __init__(self, version: int, type_id: int, bits: str) -> None:
        super().__init__(version, type_id, bits, 15)

    def should_make_more_children(self) -> bool:
        return (self.length - self.header_length) < self.children_stop_value


class OperatorPacket1(OperatorPacket):
    def __init__(self, version: int, type_id: int, bits: str) -> None:
        super().__init__(version, type_id, bits, 11)

    def should_make_more_children(self) -> bool:
        return len(self.children) < self.children_stop_value


def packet_factory(bits: str) -> Packet:
    version, type_id = read_header(bits)
    if type_id == 4:
        return LiteralPacket(version, type_id, bits)
    if bits[6] == "0":
        return OperatorPacket0(version, type_id, bits)
    if bits[6] == "1":
        return OperatorPacket1(version, type_id, bits)

    raise ValueError("Cannot determine packet type from provided bits.")


def read_header(bits: str) -> Tuple[int, int]:
    version = int(bits[:3], 2)
    type_id = int(bits[3:6], 2)

    return version, type_id


def parse_input(file: str = "input.txt") -> str:
    with open(file, "r", encoding="utf-8") as fin:
        return bin(int(fin.readline().strip(), 16))[2:]


if __name__ == "__main__":
    initial_bits = parse_input("input.txt")
    packet = packet_factory(initial_bits)
    packet.make_children()
    for idx, solution in enumerate([packet.version_sum(), packet.get_value()]):
        print(f"Solution {idx + 1}: {solution:12}")  # 951, 902198718880
