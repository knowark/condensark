from integrark import tools


def test_tools():
    assert tools.Solution is not None
    assert tools.DataLoader is not None
    assert tools.normalize is not None
    assert tools.normalize_domain is not None
