import spotipy
import csv
import time
from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_CLIENT_ID = 'insert client ID'
SPOTIPY_CLIENT_SECRET = 'insert your spotify client secret'
SPOTIPY_REDIRECT_URI = 'insert your redirect url here'

scope = "user-library-read playlist-modify-private playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))



def playlist_initializer(playlist_id):
    tracks = set()
    try:
        results = sp.playlist_tracks(playlist_id)
        for item in results['items']:
            if item['track'] and item['track']['id']:
                track_id = item['track']['id']
                track_name = item['track']['name']
                print(f"Fetching: {track_name}")  
                tracks.add(track_id)

        while results['next']:
            results = sp.next(results)
            for item in results['items']:
                if item['track'] and item['track']['id']:
                    track_id = item['track']['id']
                    track_name = item['track']['name']
                    print(f"Fetching: {track_name}")  
                    tracks.add(track_id)

    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching playlist {playlist_id}: {e}")
    except Exception as e:
        print(f"Unexpected error for playlist {playlist_id}: {e}")

    return list(tracks)



kpop_playlist_ids = [
    "1sy5Toh9YLfS78EO0licJ7", # DRIPPIN
    "7xpZVzAGm2OaNxpEPFPQSX", # ateez
    "1Z2MFFC7b6LsPYrRCUoNpv", # itzy 
    "0RoRNPtMkiPtvFJg4yaToR", # twice
    "4TnGh5PKbSjpYqpIdlW5nz", # monsta x
    "45bl5KOysDWJ6QvM99rTE5", # onewe
    "3CVYSpM7nfHFG5qCTW7Ht9", # oneus
    "3I8HGNsE2m65GaXwsarwJy", # seventeen
    "6Cn0wFvCX6VqdzRa1l0smH", # dreamcatcher
    "4q7n6N82N9j92aTmxUllTd", # TXT
    "4nScAfyDI2rjOhsWt5m5lW", # le sserafim
    "6JIoMwvCD37gWVllCFLYqe", # onf
    "43KhV6Ak1JOxruU2K7cYFo", # pentagon
    "0SVXFwa0icpE4tiqTY9igP", # onlyoneof
    "3OHJ0BNJOa2GCMkHkf1op2", # stray kids
    "2CI81WGRbuD5Niwm57e62p", # BAE173
    "4RrtMVycbzhPwhRTZ8V6c4", # trendz
    "00njLvFoUyiEC9tgPfA49q", # ive 
    "3v8Gp77alQBQvENu5U6uU3", # gidle
    "3oDR117sJqCAn1Nlz0Z8tv", # aespa
    "6JuQ2TRhIQuQshspWIqLZB", #ikon
    "2jOm3cYujQx6o1dxuiuqaX", # riize
    "7KoqftTcQaNv2yLJdOpQox", # boynextdoor
    "47tmInCWQ4Ebff8N0Zruu9", # nmixx
    "03sxfpNPwp18QXpTcc9Osm", # viviz
    "63cp4i0NPnZmHssDcAlXVs", # stayc
    "1HGibaKCSxJpZeJJyzoxol", # ace
    "1TR0xbM4GqgvyiwmQYqvUo", # enhypen
    "6oXSEQFvf5YZwRxyVfmYdV", # nct 127
    "6BS4nw07XVcONuW78DuMTw", # winner
    "7eMgP9z7meI61kSt01mJNI", # cix
    "7x0FY03BYEwCcpM9gVnGdB", # vixx
    "6tvp0QF2KK3475IyCRjaYK", # sf9
    "1SmxjL7Kn56Smy0igRjQUs", # the boyz
    "6rEAnKLtYjMsNnVbbg9jCC", # p1harmony
    "3oxqLTCxaKgRC1yvUv0E8a", # zerobaseone
    "1hJAGs532D4Z9QlYnTkeHk", # taemin
    "2ApkQAY9jjOZU0d8TL88aS", # kard
    "72vkE7HQ3UCKgRl1zzssHx", # rescene
    "3DvPjTLgBTGwnf1PcM6mdS", # artms
    "0nttPKOBraK9GrgTzEVNcq", # loona
    "0ancqLTrVS01N2GTPxjE6u", # cravity
    "5597aZeb1Xsahunrdqzyd1", # tws
    "5nMnKVIy4XarT44YZqNvRt", # xg
    "7dBCu0Vfaty1pOj0iiCB92", #wayv
    "53EjMszGloV6FhM4ymHc0W", # illit
    "6nao4rPYCxpjt0Z4NOHeru", # wei
    "2YQbP3ZwLsV2mQoDwuioIK", # just b
    "0P22NNxsPNLCMHi1naGuzM", # dkb
    "1ihpaF61TAq9WKuKD4oDJH", # kiss of life
    "1AzzoErwnmCPhT2fA6AqjJ", # babymonster
    "0jehA4H8euOq2O8I0nRDbK", # big bang
    "61nejTXnVI3VY0zUb8LadG", # exo
    "4U9cBN9vcM4rmDmgjfTSQH", # bts
    "111Tmphrp0a1xc4RmTvLkw", # red velvet
    "6UHjDWLKyv2q5nATOyai5W", # kang daniel
    "0qfzRgj7EXmgt6xPFQvNpx", # gdragon
    "406UtXzXdZRDx1CgfhMM5G", # dpr ian
    "6VqAiqJugnjAcwhYcSTuC9", #gfriend
    "4R7oZ0rWoRilNvXzvPudeU", #apink
    "3Ox4qJFeSNtyveOaylzB8K", # izone
    "210U96rc3HRasgKyho6MUU", # shinee
    "4Gy9ad70ey5qsGmXqwp0Av", # sunmi
    "4cHbGsrSMgnau91tKghpcC", # chungha
    "0vb7GZLPjfn1xIdPcQjlLC", # superjunior
    "6WHnImQq5CMhkWCFCoiBdO", #bigbang
    "72HuVG7jqUCzE06dCfSosG", # infinite
    "0GK7Qzx0zzUsIMT7N96tLN", #sistar
    "4HBAjSJ6l7gbrshF2dYUwe", # blackpink
]
kpop_playlist_ids2 = [
    "4rw4CusPM6ltWRsyT7AP9Z", # wannaone
    "1opkOn6dhncgWGq4vavttb", # treasure
    "2zgf4J3pUuvaofCajZyRHU",# & team
    "3aBfl47B8LfNKIR6WWjQQQ", # nct dream
    "6pnffWt5nSuqR7I04tG9MD", # taeyeon
    "1m0fUj9KaFpFyQJK7Sdy0i", # nct wish
    "7bSP89uh5LRyoe3jcf1gRD", # triples
    "1vzHdvD3GmYec0STIC1ICL", # kep1er
    "5UAMxteSDne9ahE9SWF9K7", #yena
    "2dvQCmXIwP2ma8mu033hTJ", #  kai
    "55l3UKvuf6SJAwBaNJPoA7", # woodz
    "3EktFq1SbZ7eU2wMHq5kU7", # mcnd
    "2VQBR9efkl23WxLFClDf7b", # ab6ix
    "2NBEWYFKOo52Y7TxTykqsw", # verivery
    "5y4aLibIvjWHjJnA4q2CeI", # beast/highlight
    "1JlEd64WXpKmTJrrfuLTd1", # omega x
    "7BFW3Gk8Wse2vXSxfZRfcn", # blitzers
    "524gh9LHCypcAQ32QJzj6C", # rocket punch
    "5YMtq5jR5qzQH8tLBWdycR", # izna
    "0gjV0FHLpcWjkFcEirNr6E", # badvillain
    "00QWHcnrnyyNoXebVDBhDD", # meov
    "6fna6ihiBsqco2dQpjzqbP", # golden child
    "5AJVeI69kbl3WbMemuHzV8", # weki meki
    "2oFohoPJAMSiULShjmdSjz", # astro
    "1bix0LSLXrmeJJ789NF7GC", # nu'est
    "0rIwOrqWza5Vmin7poAzZe", #got7
    "7jf1M3YVOcseR1BWOjrZ9W", #pristin
    "6rWdSt3Cc30Dt5DdLq21mk", # everglow
    "1JI89hUjxhzq91IrG5DUxk", # weeekly
    "0BEIoUiOWaiZIgXuabuVaZ", # the kingdom
    "1tG0Kut2gGRoAaZ7zY3fIg", # vanner
    "2kC140AasiCxn48RVChbaV", #younite
    "0druF4iZ2kqe36OkpG9cGO", #nowadays
    "0YvM6TfYJ8CN3AmVpcLGOL", #ghost9
    "486bwuGP1bPcPgDcT50Oe7", #tiot
    "6lA534viPmqNj0j8RM788s", # ampers&one
    "0da1Jd3sdkz4rQRrMJ2Gq0" # epex
    "5RqyrprYpVuN3foJZJjX3e", # waker
    "5BpDxgPzu8XdZMDMzg8qCI", # the wind
    "5Oq2Zt676qMFhq6kXlc6t5", # fantasy boys
    "7rNXwZRXSpS3rcPScmRCOi", #limelight
    "7igoCm9lSENIrtmwEaeKCG", # say my name
    "3nbNptGY6NgrTbCL1zH3t1", # issue
    "2WgJFFutZuyK8jltoAiwkq", # one pact
    "2xZalCYXY7iFV3d5ob1Gkp", # new jeans
    "0B4Di0W09uhcQuu1YdijnU", # fifty fifty
    "68qYFm2RxSU5EAaNxXGNCT", # IU
    "0mjHsajhf5HMBup6zJtsTI", # day6
    "2h5MR7Dg4l9yk00eggTG7a", # BTOB
    "49sOZPWTMmyfCdI4fXP2dN", # n.flying
    "6QJYsTJsEPeKnKpOQNQWMh", # purple kiss
    "5DJTaab13Jm14mUGuCjzFN", # wooah
    "42sKSNKO4V6Vy2619co6pM", # billlie
    "6wQo7YkOGdas1mODNMq31K", # boys republic
    "7ns9MNL3Ijn5nTAhk4Zdno", # wjsn
    "4kmqR5UiIqlCeBCAIFeTAK", # b.i
    "7C2Y6IJxy07ZHCymZnmrpK", #knk
    "2wGxO5Zn1qFKFJLo4H5glQ", # taeyong
    "55PkOaJj6pCInavIveQVXF", # 24k+
    "5x1eKXWyikvJJ5YUXkMpzu", # bloo
    "6kZxEmpfwRCN2gX97UsfdJ", # sik-k
    "58MCelDwoiOdOvhcQHF1Kj", # dean
    "7rnl75idJxvG6e3raI5oKH", # baekyun
    "1e4qq2SkOvi86gdLzhvBiT", # k-hiphop/rap
    "3GccXrkfcWeBCYh74rYKsW", # loosemble
    "72aazYtyBTi7ECINJv0g9y", # unis
    "16ajdrpjvb7pUjysE3AQ92", # h1-key
    "7BiImum6lntj4IX7b0Z57o", # evnne
    "5fN4kGCo0uFhYoIXedmn00", # xikers
    "5e3gcZtj43YGijwY0rQL7J", # tnx
    "3Qor4t7UUiJTZbw4XzlVN5", # oh my girl
    "739uqXIuM0lEENmDbX5Pnw", # cherry bullet
    "0k7ALIAtQEJRCo1q7xYM9U", # mamamoo
    "6Ca9xQc5hDaWrU8V8nvdGE", # tempest
    "6snwl3VQQaiWVq2X7uHVRn", # lun8
    "2n65tSwRlaCzWe9imln1tN", # primrose
    "1Pxasq9dt6fsV20WyTVwgH", # mimiirose
    "5RNFnijcD2aENxINY8dRO7", # xodiac
    "2PLL2mxsoG5emCEKXEOUkl", # plave
    "4lWTNPsrsb4zi85YLl8ZBk", # xlov, kenta sanggyun, n.ssign, nine.i




]

def create_playlist_and_add_songs():
    all_tracks = []

    try:
        with open('music_database.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  

            for row in reader:
                playlist_id = row[0] 

                
                tracks = playlist_initializer(playlist_id)  
                
                all_tracks.extend(tracks)  

               

    except Exception as e:
        print(f"An error occurred: {e}")

    
    username = sp.current_user()['id']  

    tracks_added = 0
    new_playlist = None

    
    for i in range(0, len(all_tracks), 100):
        batch = all_tracks[i:i + 100]

        
        if tracks_added == 0 and new_playlist is None:
            new_playlist = sp.user_playlist_create(
                user=username,
                name='all_songs_for_dataset', 
                public=False, 
                description='songs for dataset'
            )

       
        sp.playlist_add_items(new_playlist['id'], batch)  
        tracks_added += len(batch)

        if tracks_added >= 10000:
            new_playlist = sp.user_playlist_create(
                user=username,
                name=f'all_songs_for_dataset_{tracks_added // 10000 + 1}',
                public=False,
                description='songs for dataset'
            )
            tracks_added = 0  

    #
    if tracks_added > 0 and new_playlist is not None:
        sp.playlist_add_items(new_playlist['id'], all_tracks[-tracks_added:])
        

    #for i in range(0, len(all_kpop_tracks), 100):
      #  if all_kpop_tracks <= 10000: 
      #   new_playlist2 = sp.user_playlist_create(
       #  user=username, 
        # name="all_kpop_songs_for_dataset", 
        # public=False, 
        # description="Songs for dataset (kpop style)"
        #)
        
        #sp.playlist_add_items(new_playlist2['id'], all_kpop_tracks[i:i + 100])
        
    #for i in range(0, len(all_kpop_tracks), 100):
        #sp.playlist_add_items(new_playlist3['id'], all_kpop_tracks2[i:i + 100])


if __name__ == "__main__":
    
    create_playlist_and_add_songs()
  
