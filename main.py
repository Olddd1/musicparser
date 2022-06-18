import bs4
import requests
import colorama

colorama.init()

url = input('You are using a music parser. This program is open source and uses a Creative Commons license.\n'
            'Firstly, make the playlist public, then enter a link to it: ').strip()

status = requests.get(url).status_code
if status == 200:
    soup = bs4.BeautifulSoup(requests.get(url).text, "html.parser")
    tracks = soup.findAll('div', class_='d-track')
    num_tracks = len(tracks)
    print(f'The playlist contains {num_tracks} {"track" if num_tracks == 1 else "tracks"}')

    successful_downloads_num = 0
    unsuccessful_downloads_num = 0
    successful_downloads = []
    unsuccessful_downloads = []

    for i, track in enumerate(tracks):
        title = track.find('a', class_='d-track__title').text
        author = track.findAll('a', class_='deco-link_muted')[0].text
        req = requests.get(f'https://ru.hitmotop.com/search?q={title.strip().replace(" ", "+")}'
                           f'+{author.strip().replace(" ", "+")}').text
        download_buttons = bs4.BeautifulSoup(req, "html.parser").findAll('a', class_='track__download-btn')
        if download_buttons:
            url = download_buttons[0].get('href')
            with open(f'{title.strip().replace(" ", "_")}_{author.strip().replace(" ", "_")}.mp3', 'wb+') as f:
                f.write(requests.get(url).content)
            print(f'[+]{colorama.Fore.GREEN}{i + 1}/{num_tracks}, successfully: {title} {author}.{colorama.Style.RESET_ALL}')
            successful_downloads_num += 1
            successful_downloads.append(f'{title}, {author}')
        else:
            print(f'[+]{colorama.Fore.RED}{i + 1}/{num_tracks}, unsuccessfully: {title} {author}.{colorama.Style.RESET_ALL}')
            unsuccessful_downloads_num += 1
            unsuccessful_downloads.append(f'{title}, {author}')

    print(f'\nThe download is complete, {"{:02}".format(successful_downloads_num / num_tracks * 100)}'
          f'% of the tracks have been downloaded.')
    if successful_downloads_num == num_tracks:
        input('\nAll tracks downloaded successfully. Press enter to exit.')
    else:
        flag = True if input('\nDo you want to see a list of successfully downloaded tracks? [y/N]').lower() in 'yу' \
            else False
        if flag:
            print()
            for i in successful_downloads:
                print(colorama.Fore.GREEN + i + colorama.Style.RESET_ALL)
            print()

        flag = True if input('Well, do you want to see a list of unsuccessfully downloaded tracks? [y/N]').lower() \
                       in 'yу' else False

        if flag:
            print()
            for i in unsuccessful_downloads:
                print(colorama.Fore.RED + i + colorama.Style.RESET_ALL)
            print()

        input('Press enter to exit.')
else:
    print('The link is not working')



