from tools.file_reader import FileReaderTool


def make_tool(tmp_path):
    (tmp_path / "sample.txt").write_text("hello", encoding="utf-8")
    return FileReaderTool(sandbox=tmp_path)


def test_reads_file_in_sandbox(tmp_path):
    result = make_tool(tmp_path).run(path="sample.txt")
    assert result.success is True
    assert result.output == "hello"


def test_parent_folder_escape_blocked(tmp_path):
    sandbox = tmp_path / "box"
    sandbox.mkdir()
    (tmp_path / "secret.txt").write_text("secret", encoding="utf-8")
    result = FileReaderTool(sandbox=sandbox).run(path="../secret.txt")
    assert result.success is False
    assert "outside" in result.error.lower()


def test_absolute_path_blocked(tmp_path):
    outside = tmp_path / "outside.txt"
    outside.write_text("x", encoding="utf-8")
    sandbox = tmp_path / "box"
    sandbox.mkdir()
    result = FileReaderTool(sandbox=sandbox).run(path=str(outside))
    assert result.success is False


def test_missing_file(tmp_path):
    result = make_tool(tmp_path).run(path="nope.txt")
    assert result.success is False


def test_directory_is_not_a_file(tmp_path):
    (tmp_path / "folder").mkdir()
    result = make_tool(tmp_path).run(path="folder")
    assert result.success is False


def test_empty_path(tmp_path):
    result = make_tool(tmp_path).run(path="")
    assert result.success is False


def test_missing_path_input(tmp_path):
    result = make_tool(tmp_path).run()
    assert result.success is False


def test_binary_file_rejected(tmp_path):
    (tmp_path / "bin.dat").write_bytes(b"\xff\xfe\x00\x80")
    result = make_tool(tmp_path).run(path="bin.dat")
    assert result.success is False


def test_large_file_rejected(tmp_path):
    (tmp_path / "big.txt").write_text("a" * 100_001, encoding="utf-8")
    result = make_tool(tmp_path).run(path="big.txt")
    assert result.success is False
    assert "large" in result.error.lower()