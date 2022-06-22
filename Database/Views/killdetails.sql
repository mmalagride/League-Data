create view killdetails
as
select 
	ck.event_gameid as gameID,
	ROUND(ck.event_timestamp/1000) as timestamp,
	ki.summoner_name as killerID,
	vi.summoner_name as victimID,
	ai1.summoner_name as assist1_Name,
	ai2.summoner_name as assist2_Name,
	ai3.summoner_name as assist3_Name,
	ai4.summoner_name as assist4_Name,
	ck.event_killedby as killedBy,
	ck.event_posx as posX,
	ck.event_posy as posY
from 'data.championkill' ck
left join 'data.friendinfo' ki on ck.event_killerid = ki.summoner_puuid
left join 'data.friendinfo' vi on ck.event_victimid = vi.summoner_puuid
left join 'data.friendinfo' ai1 on ck.event_assist1 = ai1.summoner_puuid
left join 'data.friendinfo' ai2 on ck.event_assist2 = ai2.summoner_puuid
left join 'data.friendinfo' ai3 on ck.event_assist3 = ai3.summoner_puuid
left join 'data.friendinfo' ai4 on ck.event_assist4 = ai4.summoner_puuid