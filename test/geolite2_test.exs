defmodule ElixirPython.GeoLite2Test do
  use ExUnit.Case

  test "search" do
    results = ElixirPython.GeoLite2.search("Berlin, Germany")
    assert Enum.any?(results)
  end
end
