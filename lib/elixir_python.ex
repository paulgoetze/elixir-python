defmodule ElixirPython do
  use Export.Python

  @python_dir "lib/python"

  @doc """
  Calls the given function with args from the given Python file.
  """
  def python_call(file, function, args \\ []) do
    {:ok, py} = Python.start(python_path: Path.expand(@python_dir))
    Python.call(py, file, function, args)
  end
end
