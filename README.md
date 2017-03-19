# Examples for using Python with Elixir

The GeoLite2 example app use [erlport](https://github.com/hdima/erlport) via [export](https://github.com/fazibear/export) in order to leverage the [Whoosh](https://whoosh.readthedocs.io/en/latest/) text indexing and search Python package.

It creates a search index from the free [GeoLite2](http://dev.maxmind.com/geoip/geoip2/geolite2/) city database and provides an Elixir module to search the city index.

## Installation

* Install Python v3.x
* Install Elixir v1.4+
* Setup a [virtualenv](https://virtualenv.pypa.io) and activate it
* Run `pip install -r requirements.txt` to install the python dependencies
* Run `mix deps.get` to install the Hex dependencies


## Creating the index

Step into the interactive Elixir console with `iex -S mix`.

Then run the following function to create the city index:

```elixir
ElixirPython.GeoLite2.create_index()
```

## Searching

You can search your city index with the following code:

```elixir
iex(1)> ElixirPython.GeoLite2.search("Berlin")
[%{city: "Berlin", country: "Germany", state: "Land Berlin"},
 %{city: "Berlingen", country: "Belgium", state: "Flanders"},
 %{city: "Falkenberg", country: "Germany", state: "Land Berlin"},
 %{city: "Gosen", country: "Germany", state: "Land Berlin"},
 %{city: "Bernau bei Berlin", country: "Germany", state: "Brandenburg"},
 %{city: "Berlingen", country: "Switzerland", state: "Thurgau"},
 %{city: "Treptow Bezirk", country: "Germany", state: "Land Berlin"},
 %{city: "Heinersdorf", country: "Germany", state: "Land Berlin"},
 %{city: "Stirling", country: "Canada", state: "Alberta"},
 %{city: "New Berlin", country: "United States", state: "Illinois"}]


```

The default number of returned results is 10.  
You can also pass the number of wanted results as the second argument:

```elixir
iex(2)> ElixirPython.GeoLite2.search("Berlin", 3)
[%{city: "Berlin", country: "Germany", state: "Land Berlin"},
 %{city: "Berlingen", country: "Belgium", state: "Flanders"},
 %{city: "Falkenberg", country: "Germany", state: "Land Berlin"}]
```
