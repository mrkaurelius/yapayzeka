# yapayzeka

Takviyeli öğrenme ile labirentte yol bulma uygulamaları

### kaynaklar

- https://gym.openai.com/docs/
- https://github.com/MattChanTK/gym-maze
- https://github.com/MattChanTK/ai-gym/blob/master/maze_2d/maze_2d_q_learning.py

### yukleme
virtual environment'in kurulmasi PyPI bagimliliklarinin yuklenmesi
```bash
git clone git clone --recursive https://github.com/mrkaurelius/yapayzeka
cd yapayzeka
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

#### gym-maze
PyPI de olmayan gym-maze kutuphanesinin yuklenmesi.
```
cd yapayzeka
cd lib/gym-maze
python3 setup.py install
```

Debian 10 Busterda test edildi. Debian tabanli dagitimlarda sorunsuz calismasi gerekir.