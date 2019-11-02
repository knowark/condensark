from integrark import tools


def test_tools():
    assert tools.Solution is not None
    assert tools.DataLoader is not None
    assert tools.StandardDataLoader is not None
    assert tools.parse_domain is not None
