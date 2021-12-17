"""https://adventofcode.com/2021/day/16"""

from abc import ABC, abstractmethod
from typing import Tuple, List
import math


class Packet(ABC):
    def __init__(self, bits: str) -> None:
        self.bits = bits
        self.version, self.type_id = read_header(bits)
        self.children: List["Packet"] = []
        self.consumed_by_children = 0
        self.value = 0

    @abstractmethod
    def trailing_data(self) -> str:
        ...

    @abstractmethod
    def make_children(self) -> str:
        ...

    def version_sum(self) -> int:
        total = self.version
        for child in self.children:
            total += child.version_sum()

        return total

    def get_value(self) -> int:
        if not self.children:
            return self.value

        if self.type_id == 0:
            return sum(c.get_value() for c in self.children)
        if self.type_id == 1:
            return math.prod(c.get_value() for c in self.children)
        if self.type_id == 2:
            return min(c.get_value() for c in self.children)
        if self.type_id == 3:
            return max(c.get_value() for c in self.children)

        first, second, *_ = self.children
        if self.type_id == 5:
            return int(first.get_value() > second.get_value())
        if self.type_id == 6:
            return int(first.get_value() < second.get_value())
        if self.type_id == 7:
            return int(first.get_value() == second.get_value())

        raise ValueError(f"Unknown type id: {self.type_id}")


class PacketLiteral(Packet):
    def __init__(self, bits: str) -> None:
        super().__init__(bits)
        self.value, self._data_size = self._parse_data()

    def _parse_data(self) -> Tuple[int, int]:
        bit_groups = []
        for i in range(6, len(self.bits), 5):
            group = self.bits[i : i + 5]
            bit_groups.append(group[1:])
            if group[0] == "0":
                break

        bit_string = "".join(bit_groups)
        value = int(bit_string, 2)
        i = 6 + len(bit_string) + len(bit_groups)

        return value, i

    def trailing_data(self) -> str:
        return self.bits[self._data_size :]

    def make_children(self) -> str:
        return self.trailing_data()


class PacketOperator(Packet):
    @property
    @abstractmethod
    def type_bits_count(self) -> int:
        ...

    @abstractmethod
    def should_make_more_children(self) -> bool:
        ...

    def trailing_data(self) -> str:
        i = 6 + 1 + self.type_bits_count
        return self.bits[i:]

    def make_children(self) -> str:
        data = self.trailing_data()
        while self.should_make_more_children():
            child = packet_factory(data)
            data_after_child = child.make_children()
            self.consumed_by_children += len(data) - len(data_after_child)
            data = data_after_child
            self.children.append(child)
        return self.trailing_data()[self.consumed_by_children :]


class PacketOp0(PacketOperator):
    @property
    def type_bits_count(self) -> int:
        return 15

    def should_make_more_children(self) -> bool:
        for_children = int(self.bits[6 + 1 : 6 + 1 + self.type_bits_count], 2)
        return self.consumed_by_children < for_children


class PacketOp1(PacketOperator):
    @property
    def type_bits_count(self) -> int:
        return 11

    def should_make_more_children(self) -> bool:
        needed_children = int(self.bits[6 + 1 : 6 + 1 + self.type_bits_count], 2)
        return len(self.children) < needed_children


def packet_factory(bits: str) -> Packet:
    _, type_id = read_header(bits)
    if type_id == 4:
        return PacketLiteral(bits)

    if bits[6] == "0":
        return PacketOp0(bits)

    if bits[6] == "1":
        return PacketOp1(bits)

    raise ValueError("Cannot determine packet type from provided bits.")


def read_header(bits: str) -> Tuple[int, int]:
    version = int(bits[:3], 2)
    type_id = int(bits[3:6], 2)

    return version, type_id


def padded_length(number: int, chunk_size: int = 4) -> int:
    full, rem = divmod(number, chunk_size)
    return (full + 1) * chunk_size if rem else full * chunk_size


def parse_input(file: str = "input.txt") -> str:
    with open(file, "r", encoding="utf-8") as fin:
        bit_string = bin(int(fin.readline().strip(), 16))[2:]
        bit_string = bit_string.zfill(padded_length(len(bit_string)))

        return bit_string


if __name__ == "__main__":
    initial_bits = parse_input("input.txt")
    packet = packet_factory(initial_bits)
    packet.make_children()
    print(packet.version_sum())  # 951
    print(packet.get_value())  # 902198718880
