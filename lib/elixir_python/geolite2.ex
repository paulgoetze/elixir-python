defmodule ElixirPython.GeoLite2 do
  import ElixirPython, only: [python_call: 2, python_call: 3]

  @python_module "geolite2"

  @doc """
  Creates search index from raw csv data
  """
  def create_index() do
    python_call(@python_module, "create_index")
  end

  @doc """
  Returns a list of the highest ranked `count` results from the index.
  """
  def search(query, count \\ 10) do
    query = clean_text(query)
    results = python_call(@python_module, "search", [query, count])

    for [city, state, country] <- results do
      %{city: "#{city}", state: "#{state}", country: "#{country}"}
    end
  end

  defp clean_text(text) do
    :iconv.convert("utf-8", "ascii//translit", text)
  end
end
