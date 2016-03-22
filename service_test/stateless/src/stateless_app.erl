%%%-------------------------------------------------------------------
%% @doc stateless public API
%% @end
%%%-------------------------------------------------------------------

-module(stateless_app).

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
    {ok, _} = epgsql_pool:start(stateless_pool, 10, 10, Params),
    Routes = [
        {'_', [
            {"/", http_stateless, []}
        ]}
    ],
    Dispatch = cowboy_router:compile(Routes),
    {ok, _} = cowboy:start_http(http, 200, [{port, 8888}], [{env, [{dispatch, Dispatch}]}]),
    stateless_sup:start_link().

%%--------------------------------------------------------------------
stop(_State) ->
    ok.

%%====================================================================
%% Internal functions
%%====================================================================
