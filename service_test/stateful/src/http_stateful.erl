-module(http_stateful).

-export([init/3]).
-export([handle/2]).
-export([terminate/3]).
-define(EMAIL, <<"vasya@tut.by">>).

init(_Type, Req, []) ->
    {ok, Req, undefined}.

handle(Req, State) ->
    [{?EMAIL, PlayerInfo}] = ets:lookup(players, ?EMAIL),
    %%io:format("PlayerInfo is ~p~n", [PlayerInfo]),
    JsonPlayerInfo = jiffy:encode(PlayerInfo),
    {ok, Req2} = cowboy_req:reply(200, [
            {<<"content-type">>, <<"text/plain">>}
    ], JsonPlayerInfo, Req),
    {ok, Req2, State}.

terminate(_Reason, _Req, _State) ->
    ok.
