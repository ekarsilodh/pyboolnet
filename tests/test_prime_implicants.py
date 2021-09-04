

import pytest

import PyBoolNet


@pytest.mark.parametrize("copy", [True, False])
def test_remove_variables(copy):

    primes = PyBoolNet.file_exchange.bnet2primes("v1, v1 \n v2, v1")
    x = PyBoolNet.prime_implicants.remove_variables(primes, ["v2"], in_place=copy)
    answer = x if copy else primes

    assert answer == {"v1": [[{"v1": 0}], [{"v1": 1}]]}


@pytest.mark.parametrize("copy", [True, False])
def test_remove_all_variables_except(copy):

    primes = PyBoolNet.file_exchange.bnet2primes("v1, v1 \n v2, v1")
    x = PyBoolNet.prime_implicants.remove_all_variables_except(primes, ["v1"], in_place=copy)
    answer = x if copy else primes

    assert answer == {"v1": [[{"v1": 0}], [{"v1": 1}]]}


@pytest.mark.parametrize("copy", [True, False])
def test_rename(copy):

    primes = PyBoolNet.Repository.get_primes("raf")
    x = PyBoolNet.prime_implicants.rename_variable(primes, "Raf", "Raf23", Copy=copy)
    answer = x if copy else primes

    expected = {"Raf23": [[{"Raf23": 1, "Erk": 1}], [{"Raf23": 0}, {"Erk": 0}]], "Mek": [[{"Raf23": 0, "Erk": 0}, {"Mek": 0, "Erk": 0}], [{"Mek": 1, "Raf23": 1}, {"Erk": 1}]], "Erk": [[{"Raf23": 0, "Erk": 0}, {"Mek": 0}], [{"Mek": 1, "Raf23": 1}, {"Mek": 1, "Erk": 1}]]}

    assert answer == expected

    with pytest.raises(Exception):
        PyBoolNet.prime_implicants.rename_variable(primes, "GADD", "GADD12")


def test_create_disjoint_union():
    primes1 = PyBoolNet.file_exchange.bnet2primes("A, B \n B, !A")
    primes2 = PyBoolNet.file_exchange.bnet2primes("C, D \n D, C")
    primes = PyBoolNet.file_exchange.bnet2primes("A, B \n B, !A \n C, D \n D, C")
    result = PyBoolNet.prime_implicants.create_disjoint_union(primes1, primes2)

    assert result == primes

    primes1 = PyBoolNet.file_exchange.bnet2primes("A, B \n B, !A")
    primes2 = PyBoolNet.file_exchange.bnet2primes("C, B \n D, C")

    with pytest.raises(Exception):
        PyBoolNet.prime_implicants.create_disjoint_union(primes1, primes2)


@pytest.mark.parametrize("copy", [True, False])
def test_remove_variables(copy):

    primes = PyBoolNet.file_exchange.bnet2primes("A, !C|B \n B, 0 \n C, 1")
    x = PyBoolNet.prime_implicants.remove_variables(primes, ["A", "B", "C"], in_place=copy)
    answer = x if copy else primes

    assert PyBoolNet.prime_implicants.are_equal({}, answer)


@pytest.mark.parametrize("copy", [True, False])
def test_remove_variables_except(copy):

    primes = PyBoolNet.file_exchange.bnet2primes("A, !C|B \n B, 0 \n C, 1")
    x = PyBoolNet.prime_implicants.remove_variables(primes=primes, names=[], in_place=copy)
    answer = x if copy else primes

    assert PyBoolNet.prime_implicants.are_equal(answer, primes)

    primes = PyBoolNet.file_exchange.bnet2primes("A, !C|B \n B, 0 \n C, 1")
    x = PyBoolNet.prime_implicants.remove_all_variables_except(primes=primes, names=["B", "C"], in_place=copy)
    answer = x if copy else primes

    expected = PyBoolNet.file_exchange.bnet2primes("B, 0 \n C, 1")

    assert PyBoolNet.prime_implicants.are_equal(expected, answer)

    primes = PyBoolNet.file_exchange.bnet2primes("A, !C|B \n B, 0 \n C, 1")

    with pytest.raises(Exception):
        PyBoolNet.prime_implicants.remove_variables(primes, ["B"], in_place=copy)


@pytest.mark.parametrize("copy", [True, False])
def test_create_variables1(copy):
    primes = PyBoolNet.file_exchange.bnet2primes("v1, v1 \n v2, v1")
    x = PyBoolNet.prime_implicants.create_variables(primes, {"v1": "v2"}, in_place=copy)
    answer = x if copy else primes

    assert answer == {"v1": [[{"v2": 0}], [{"v2": 1}]], "v2": [[{"v1": 0}], [{"v1": 1}]]}


@pytest.mark.parametrize("copy", [True, False])
def test_create_variables2(copy):
    primes = PyBoolNet.file_exchange.bnet2primes("v1, v1 \n v2, v1")
    x = PyBoolNet.prime_implicants.create_variables(primes, {"v1": lambda v2: not v2}, in_place=copy)
    answer = x if copy else primes

    assert answer == {"v1": [[{"v2": 1}], [{"v2": 0}]], "v2": [[{"v1": 0}], [{"v1": 1}]]}


@pytest.mark.parametrize("copy", [True, False])
def test_create_variables3(copy):
    primes = PyBoolNet.file_exchange.bnet2primes("v1, v1 \n v2, v1")
    x = PyBoolNet.prime_implicants.create_variables(primes, {"v3": "v2", "v4": lambda v3: v3}, in_place=copy)
    answer = x if copy else primes

    assert answer == {"v1": [[{"v1": 0}], [{"v1": 1}]],  "v2": [[{"v1": 0}], [{"v1": 1}]],  "v3": [[{"v2": 0}], [{"v2": 1}]],  "v4": [[{"v3": 0}], [{"v3": 1}]]} 


def test_create_variables4():
    primes = PyBoolNet.file_exchange.bnet2primes("v1, v1 \n v2, v1")
    with pytest.raises(Exception):
        PyBoolNet.prime_implicants.create_variables(primes, {"v3": "v4"})


def test_input_combinations1():
    primes = PyBoolNet.file_exchange.bnet2primes("input1, input1 \n input2, input2")

    expected = [{"input1": 0, "input2": 0}, {"input1": 0, "input2": 1}, {"input1": 1, "input2": 0}, {"input1": 1, "input2": 1}]
    expected.sort(key=lambda x: tuple(sorted(x.items())))
    answer = list(PyBoolNet.prime_implicants.input_combinations(primes))
    answer.sort(key=lambda x: tuple(sorted(x.items())))

    assert answer == expected


def test_input_combinations2():
    primes = PyBoolNet.file_exchange.bnet2primes("v1, v2 \n v2, v1")

    assert list(PyBoolNet.prime_implicants.input_combinations(primes)) == [{}]


def test_copy():
    p1 = {"v1": [[{"v2": 0}], [{"v2": 1}]], "v2": [[{"v2": 0}, {"v1": 1}], [{"v1": 0, "v2": 1}]]}
    p2 = PyBoolNet.prime_implicants.copy_primes(p1)
    p2["v1"] = [[{"v1": 0}], [{"v1": 1}]]

    assert p1 != p2


def test_find_inputs():
    primes = {"B": [[{"B": 0}], [{"B": 1}]], "C": [[{"C": 1}], [{"C": 0}]], "A": [[{"B": 0, "C": 1}], [{"C": 0}, {"B": 1}]]}
    
    assert PyBoolNet.prime_implicants.find_inputs(primes) == ["B"]


def test_find_constants():
    primes = {"B": [[{}], []], "C": [[], [{}]], "A": [[{"B": 0, "C": 1}], [{"C": 0}, {"B": 1}]]}
    
    assert PyBoolNet.prime_implicants.find_constants(primes) == {"B": 0, "C": 1}


def test_equal():
    p1 = {"v1": [[{"v2": 0}], [{"v2": 1}]], "v2": [[{"v2": 0}, {"v1": 1}], [{"v1": 0, "v2": 1}]]}
    p2 = {"v1": [[{"v2": 0}], [{"v2": 1}]], "v2": [[{"v1": 1}, {"v2": 0}], [{"v2": 1, "v1": 0}]]}

    assert PyBoolNet.prime_implicants.are_equal(p1, p2)


def test_percolation():
    primes = PyBoolNet.file_exchange.bnet2primes("A, 0 \n B, A")

    assert PyBoolNet.prime_implicants.percolate_and_keep_constants(primes) == {"A": 0, "B": 0}

    primes = PyBoolNet.file_exchange.bnet2primes("A, 0 \n B, A")

    assert PyBoolNet.prime_implicants.percolate_and_remove_constants(primes) == {"A": 0, "B": 0}


def test_percolation1a():
    primes = {"A": [[{}], []], "B": [[{}], []], "C": [[{"A": 1}, {"B": 0}], [{"A": 0, "B": 1}]]}
    PyBoolNet.prime_implicants.percolate_and_remove_constants(primes)

    assert PyBoolNet.prime_implicants.are_equal({}, primes)


def test_percolation1b():
    primes = {"A": [[{}], []], "B": [[{}], []], "C": [[{"A": 1}, {"B": 0}], [{"A": 0, "B": 1}]]}
    PyBoolNet.prime_implicants.percolate_and_keep_constants(primes)
    expected = {"A": [[{}], []], "B": [[{}], []], "C": [[{}], []]}

    assert PyBoolNet.prime_implicants.are_equal(expected, primes)


def test_percolation2a():
    primes = {"A": [[{}], []], "B": [[], [{}]], "C": [[{"A": 1}, {"B": 0}], [{"A": 0, "B": 1}]]}
    PyBoolNet.prime_implicants.percolate_and_remove_constants(primes)

    assert PyBoolNet.prime_implicants.are_equal({}, primes)


def test_percolation2b():
    primes = {"A": [[{}], []], "B": [[], [{}]], "C": [[{"A": 1}, {"B": 0}], [{"A": 0, "B": 1}]]}
    PyBoolNet.prime_implicants.percolate_and_keep_constants(primes)
    expected = {"A": [[{}], []], "B": [[], [{}]], "C": [[], [{}]]}

    assert PyBoolNet.prime_implicants.are_equal(expected, primes)


def test_percolation3a():
    primes = {"A": [[{}], []], "B": [[{"A": 1}], [{"A": 0}]], "C": [[{"B": 0}], [{"B": 1}]]}
    PyBoolNet.prime_implicants.percolate_and_remove_constants(primes)

    assert PyBoolNet.prime_implicants.are_equal({}, primes)


def test_percolation3b():
    primes = {"A": [[{}], []], "B": [[{"A": 1}], [{"A": 0}]], "C": [[{"B": 0}], [{"B": 1}]]}
    PyBoolNet.prime_implicants.percolate_and_keep_constants(primes)
    expected = {"A": [[{}], []], "B": [[], [{}]], "C": [[], [{}]]}

    assert PyBoolNet.prime_implicants.are_equal(expected, primes)


def test_percolation4a():
    primes = {"A": [[{"A": 0}], [{"A": 1}]], "B": [[{"A": 1}], [{"A": 0}]], "C": [[{"B": 0}], [{"B": 1}]]}
    PyBoolNet.prime_implicants.percolate_and_remove_constants(primes)
    expected = {"A": [[{"A": 0}], [{"A": 1}]], "B": [[{"A": 1}], [{"A": 0}]], "C": [[{"B": 0}], [{"B": 1}]]}

    assert PyBoolNet.prime_implicants.are_equal(expected, primes), str(primes) + " vs " + str(expected)


def test_percolation4b():
    primes = {"A": [[{"A": 0}], [{"A": 1}]], "B": [[{"A": 1}], [{"A": 0}]], "C": [[{"B": 0}], [{"B": 1}]]}
    expected = PyBoolNet.prime_implicants.copy_primes(primes)
    PyBoolNet.prime_implicants.percolate_and_keep_constants(primes)

    assert PyBoolNet.prime_implicants.are_equal(expected, primes), str(primes) + " vs " + str(expected)


def test_create_blinkers():
    primes = {"A": [[{"A": 0}], [{"A": 1}]], "B": [[{"A": 1}], [{"A": 0}]], "C": [[{"B": 0}], [{"B": 1}]]}
    PyBoolNet.prime_implicants.create_blinkers(primes=primes, names=["A"])
    expected = primes = {"A": [[{"A": 1}], [{"A": 0}]], "B": [[{"A": 1}], [{"A": 0}]], "C": [[{"B": 0}], [{"B": 1}]]}

    assert PyBoolNet.prime_implicants.are_equal(expected, primes), str(primes) + " vs " + str(expected)

def test_active_primes():
    primes = {"A": [[{"A": 0}], [{"A": 1}]], "B": [[{"A": 1}], [{"A": 0}]], "C": [[{"B": 0}], [{"B": 1}]]}
    subspace1 = {"A":1}
    subspace2 = {'A': 1, 'B': 0, 'C': 1}
    subspace3 = {} 
    
    assert PyBoolNet.prime_implicants.active_primes(primes, subspace1) == {"A": [[], [{"A": 1}]], "B": [[{"A": 1}], []], "C": [[{"B": 0}], [{"B": 1}]]}
    assert PyBoolNet.prime_implicants.active_primes(primes, subspace2) == {"A": [[], [{"A": 1}]], "B": [[{"A": 1}], []], "C": [[], []]}
    assert PyBoolNet.prime_implicants.active_primes(primes, subspace3) == primes


