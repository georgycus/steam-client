import steam


def test_steam_package_imports_after_distribution_rename():
    assert isinstance(steam.__version__, str)
    assert steam.__version__
