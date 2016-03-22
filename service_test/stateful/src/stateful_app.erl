%%%-------------------------------------------------------------------
%% @doc stateful public API
%% @end
%%%-------------------------------------------------------------------

-module(stateful_app).

-behaviour(application).

%% Application callbacks
-export([start/2
        ,stop/1]).

%%====================================================================
%% API
%%====================================================================

start(_StartType, _StartArgs) ->
    Params = #{
        host => "localhost",
        port => 5433,
        username => "wgm",
        password => "wgm",
        database => "test"
    },
    {ok, _} = epgsql_pool:start(stateful_pool, 10, 10, Params),

    ets:new(players, [set, named_table, protected, {read_concurrency, true}]),
    {ok, _, PlayerList} = epgsql_pool:query(stateful_pool, <<"SELECT * FROM player">>),
    io:format("PlayerList is ~p~n", [PlayerList]),
    lists:map(
        fun(RawPlayerInfo) -> 
            io:format("RawPlayerInfo is ~p~n", [RawPlayerInfo]),
            Email = element(3, RawPlayerInfo),
            PlayerInfo = #{
                <<"id">> => element(1, RawPlayerInfo),
                <<"name">> => element(2, RawPlayerInfo),
                <<"email">> => Email
            },
            ets:insert(players, {Email, PlayerInfo})
        end, PlayerList),

    Routes = [
        {'_', [
            {"/", http_stateful, []}
        ]}
    ],
    Dispatch = cowboy_router:compile(Routes),
    {ok, _} = cowboy:start_http(http, 200, [{port, 8888}], [{env, [{dispatch, Dispatch}]}]),
    stateful_sup:start_link().

%%--------------------------------------------------------------------
stop(_State) ->
    ok.

%%====================================================================
%% Internal functions
%%====================================================================
