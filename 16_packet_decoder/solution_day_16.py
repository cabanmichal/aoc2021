"""https://adventofcode.com/2021/day/16"""

import math
from abc import ABC, abstractmethod
from typing import Tuple, List


class Packet(ABC):
    def __init__(self, version: int, type_id: int, bits: str) -> None:
        self.version = version
        self.type_id = type_id
        self.bits = bits
        self.children: List["Packet"] = []
        self.consumed_by_children = 0

    @abstractmethod
    def trailing_data(self) -> str:
        """Return bits that should be used for parsing other Packets."""

    @abstractmethod
    def make_children(self) -> str:
        """Create child Packets and return bits they didn't use."""

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


class LiteralPacket(Packet):
    def __init__(self, version: int, type_id: int, bits: str) -> None:
        super().__init__(version, type_id, bits)
        self._value, self._data_size = self._parse_data()

    def _parse_data(self) -> Tuple[int, int]:
        bit_groups = []
        for i in range(6, len(self.bits), 5):
            group = self.bits[i : i + 5]
            bit_groups.append(group[1:])
            if group[0] == "0":
                break

        bit_string = "".join(bit_groups)
        value = int(bit_string, 2)
        data_size = 6 + len(bit_string) + len(bit_groups)

        return value, data_size

    def trailing_data(self) -> str:
        return self.bits[self._data_size :]

    def make_children(self) -> str:
        return self.trailing_data()

    def get_value(self) -> int:
        return self._value


class OperatorPacket(Packet):
    def __init__(
        self, version: int, type_id: int, bits: str, type_bits_count: int
    ) -> None:
        super().__init__(version, type_id, bits)
        self.type_bits_count = type_bits_count
        self.children_stop_value = int(
            self.bits[6 + 1 : 6 + 1 + self.type_bits_count], 2
        )

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
            self.children.append(child)
            data_after_child = child.make_children()
            self.consumed_by_children += len(data) - len(data_after_child)
            data = data_after_child
        return self.trailing_data()[self.consumed_by_children :]


class OperatorPacket0(OperatorPacket):
    def __init__(self, version: int, type_id: int, bits: str) -> None:
        super().__init__(version, type_id, bits, 15)

    def should_make_more_children(self) -> bool:
        return self.consumed_by_children < self.children_stop_value


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


def padded_length(number: int, chunk_size: int = 4) -> int:
    """Return closest gte multiple of chunk_size."""
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
    for idx, solution in enumerate([packet.version_sum(), packet.get_value()]):
        print(f"Solution {idx + 1}: {solution:12}")  # 951, 902198718880
