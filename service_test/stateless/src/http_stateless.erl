-module(http_stateless).

-export([init/3]).
-export([handle/2]).
-export([terminate/3]).

init(_Type, Req, []) ->
    {ok, Req, undefined}.

handle(Req, State) ->
    {ok, _, [RawPlayerInfo]} = epgsql_pool:query(stateless_pool, <<"SELECT * FROM player WHERE email=$1">>, 
                                                [<<"vasya@tut.by">>]),
    %%io:format("RawPlayerInfo is ~p~n", [RawPlayerInfo]),
    PlayerInfo = #{
        <<"id">> => element(1, RawPlayerInfo),
        <<"name">> => element(2, RawPlayerInfo),
        <<"email">> => element(3, RawPlayerInfo)
    },
    JsonPlayerInfo = jiffy:encode(PlayerInfo),
    {ok, Req2} = cowboy_req:reply(200, [
            {<<"content-type">>, <<"text/plain">>}
    ], JsonPlayerInfo, Req),
    {ok, Req2, State}.

terminate(_Reason, _Req, _State) ->
    ok.
