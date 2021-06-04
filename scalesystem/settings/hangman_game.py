from unidecode import unidecode
import os
import telebot
import urllib
import json

bot = telebot.TeleBot("1795039941:AAEkGr4y5CAQbSg7Ul85SoLo2DjlIv0XanU")

hanged = {'head' : "O",'body' : "|",'left_arm' : "/",'right_arm' : "\\",'left_leg' : "/",'right_leg' : "\\",'cut' : "_"}
empty  = {'head' : " ",'body' : " ",'left_arm' : " ",'right_arm' : " ", 'left_leg' : " ",'right_leg' : " ", 'cut' : " "}

class Player:
    array = []
    def __init__(self,id,first):
        self.id = id
        self.first = first
        self._hang = 0
        self.round_win = 0
    def wrong(self):
        self._hang +=1
        return self
    def hang(self):
        hang_number = self._hang
        ret = "```-|----|\n |    |\n |   "
        ret += empty['cut'] if hang_number < 7 else hanged['cut']
        ret += empty['head'] if hang_number < 1 else hanged['head']
        ret += empty['cut'] if hang_number < 7 else hanged['cut']
        ret += "\n |   "
        ret += empty['left_arm'] if hang_number < 3 else hanged['left_arm']
        ret += empty['body'] if hang_number < 2 else hanged['body']
        ret += empty['right_arm'] if hang_number < 4 else hanged['right_arm']
        ret += "\n |    "
        ret += empty['body'] if hang_number < 2 else hanged['body']
        ret += "\n |   "
        ret += empty['left_leg'] if hang_number < 5 else hanged['left_leg']
        ret += " "
        ret += empty['right_leg'] if hang_number < 6 else hanged['right_leg']
        ret += "\n |  "
        ret += empty['left_leg'] if hang_number < 5 else hanged['left_leg']
        ret += "   "
        ret += empty['right_leg'] if hang_number < 6 else hanged['right_leg']
        ret += "\n |\n_|____```"
        return ret
    def __eq__(self, other): 
        if not isinstance(other, Player):
            return NotImplemented

        return self.id == other.id
    
    def chef():
        return Player.array[par['chef']]
    def turn():
        return Player.array[par['turn']]
    def score():
        ret = "Placar de pontos:\n\tPontos\tChances\n"
        for i in Player.array:
            ret+= "Nome: "+i.first+"; Pontos: "+str(i.round_win)+"; Chances: "+str(7-i._hang)+"\n"
        return ret
    def broadcast(message):
        for i in Player.array:
            bot.send_message(i.id,message)


already_used = []

word = {'origin':"",
        'normal':"",
        'mask'  :""}

par = {
    'chef':0,
    'turn':1,
    'waiting_word':0,
    'round':0
}

def available():
    ret = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in already_used:
        ret = ret.replace(i,' ')
    return ret

def define_word(w):
    if "_" in w:
        return False
    word['origin'] = w
    word['normal'] = unidecode(w).upper()
    word['mask'] = ""
    for i in w:
        word['mask']+= "_" if unidecode(i).isalpha() else i
    return True

def letter_recive(letter):
    letter = unidecode(letter).upper()
    already_used.append(letter)
    mask = ""
    match = False
    for o,n,m in zip(word['origin'], word['normal'],word['mask']):
        if letter == n:
            match = True
            mask += o
        else:
            mask += m
    word['mask'] = mask

    return match

def end_game():
    ended = True
    for i in Player.array:
        if i != Player.chef() and i._hang < 7:
            ended = False
    if ended:
        return True
    else:
        return "_" not in word['mask']

def next_player():
    par['turn'] +=1
    par['turn'] = par['turn']-len(Player.array)
    while par['turn'] < len(Player.array) and (Player.turn() == Player.chef() or Player.turn()._hang>=7):
        par['turn'] +=1
    if par['turn']<0 :
        par['turn'] += len(Player.array)

    

def board(player):
    ret = "Disponiveis: "+ available()+"\n"
    ret += player.hang() + "\n"
    return ret

def reset_game():
    already_used.clear()
    for i in Player.array:
        i._hang = 0

    word['origin'] = ""
    word['normal'] = ""
    word['mask'] = ""

def process():
    if len(Player.array) < 1:
        Player.broadcast("Precisamos de mais uma pessoa para jogar")
    else:
        if end_game():
            par['round']+=1
            if(not par['waiting_word']):
                if par['round'] ==1:
                    bot.send_message(Player.chef().id,"Me diz uma palavra pra a gente brincar.")
                else:
                    Player.broadcast("A palavra era: "+word['origin']+"\n Agora inicaremos outra rodada.")
                    bot.send_message(Player.chef().id,"Me diz outra palavra pra a gente brincar de novo.")
                par['waiting_word'] = True
            reset_game()
            next_player()
        else:
            bot.send_message(Player.turn().id, board(Player.turn()),parse_mode = "Markdown")
            bot.send_message(Player.turn().id,"Palavra: "+word["mask"])
            bot.send_message(Player.turn().id, "Qual letra você quer?")

@bot.message_handler(commands=['start','help'])
def send_start_message(message):
    bot.reply_to(message, "Olá, eu sou Michele!\n\nEstamos jogando o jogo da forca. Se quiser jogar conosco, envie um 'oi' para se inscrever.")

@bot.message_handler(commands=['score'])
def send_score_message(message):
    bot.reply_to(message, Player.score())

@bot.message_handler(commands=['out'])
def send_out_message(message):
    p = Player(message.from_user.id,message.from_user.first_name)
    index = Player.array.index(p)
    bot.reply_to(message, "Obrigado por jogar. Até a próxima.")
    Player.array.pop(index)
    Player.broadcast("Um instante pessoal. "+p.first+" saiu do jogo. Precisaremos reiniciar a rodada.")
    reset_game()
    if par['chef']> index:
        par['chef'] -= 1
    if par['turn']>= len(Player.array):
        par['turn'] = len(Player.array)-1
    process()


@bot.message_handler(commands=['reset'])
def send_reset_message(message):
    p = Player(message.from_user.id,message.from_user.first_name)
    if p in Player.array:
        reset_game()
        Player.array.clear()
        par['turn'] = 0
        par['chef'] = 0
        par['waiting_word'] = False
        bot.reply_to(message, "Reiniciado")
    else:
        send_start_message(message)
    

@bot.message_handler(regexp=".*([oO]i.*)|([oO]l[aá].*).*")
def handle_message(message):
    p = Player(message.from_user.id,message.from_user.first_name)
    if p not in Player.array:
        bot.send_message(p.id, "Olá, "+ p.first +"! Eu sou a Michele.")
        if len(Player.array)==0 :
            bot.send_message(p.id, "Eu estava aguardando pessoas para brincar de jogo da forca comigo. Você é o primeiro.")
            bot.send_message(p.id, "Enquanto aguardamos os outros jogadores, vou explicar como vamos brincar.\n\nComo você é o primeiro, você começará definindo a palavra. Daí, todos os outros jogadores vão receber os digitos mascarados com '_', as suas respectivas forcas e todas as letras que ja foram usadas, cada um na sua devida vez. Cada um terá direito de errar apenas 6 vezes. O sétimo erro o custara a vida!")
        else:
            bot.send_message(p.id, "Seja bem vindo ao nosso jogo da forca. Aguarde que lhe enviarei a palavra do jogo junto com sua forca.")
            bot.send_message(p.id, "Enquanto isso, vou explicar como vamos brincar.\n\nO primeiro jogador começará definindo a palavra. Daí, todos os outros jogadores, incluindo você,  vão receber os digitos mascarados com '_', as suas respectivas forcas e todas as letras que ja foram usadas, cada um na sua devida vez. Cada um terá direito de errar apenas 6 vezes. O sétimo erro o custara a vida!")
            process()
        Player.array.append(p)
    else:
        bot.send_message(p.id,"Você ja está no jogo, por favor, aguarde a sua vez!!")

@bot.message_handler(regexp=".*")
def handle_message(message):
    p = Player(message.from_user.id,message.from_user.first_name)
    if p not in Player.array:
        bot.send_message(p.id, "Estamos jogando o jogo da forca. Se quiser jogar conosco, envie um 'oi' para se inscrever.")
    else:
        if par['waiting_word'] and p == Player.chef():
            define_word(message.text)
            bot.send_message(p.id,"Palavra definida!")
            par['waiting_word'] = False
            process()
        elif len(Player.array) > 1 and p == Player.turn():
            p = Player.turn()
            letter = unidecode(message.text[0]).upper()
            if letter not in already_used:
                if letter_recive(letter):
                    if(end_game()):
                        bot.send_message(p.id, "Parabéns! Você acertou a palavra! Você será o próximo a escolher a palavra!")
                        Player.broadcast(p.first+" acertou a palavra completa e se livrou da forca.")
                        bot.send_message(Player.chef().id,"Agora é você que vai pra forca!")
                        p.round_win+=1
                        par['chef'] = Player.array.index(p)

                    else:
                        bot.send_message(p.id, "Parabéns! Você acertou a letra, viverá mais alguns intantes, mas você ainda está na forca!")
                        bot.send_message(Player.chef().id,p.first+" acertou na vez dele. Olha como ele tá.")
                        bot.send_message(Player.chef().id,board(p),parse_mode = "Markdown")
                        bot.send_message(Player.chef().id,"Palavra: "+word["mask"])
                        next_player()
                else:
                    p.wrong()
                    if(p._hang <7):
                        bot.send_message(p.id, "Vish!! Errou!! Você esta mais próximo de morrer.")
                        bot.send_message(Player.chef().id,p.first+" errou na vez dele. Olha como ele tá.")
                        bot.send_message(Player.chef().id,board(p),parse_mode = "Markdown")
                        bot.send_message(Player.chef().id,"Palavra: "+word["mask"])
                        next_player()
                    else:
                        bot.send_message(p.id,board(p),parse_mode = "Markdown")
                        bot.send_message(p.id, "Você morreu!! É uma pena mas "+ Player.chef().first+" chutou seu banco da forca. Espere para ressucitar na próxima rodada!")
                        bot.send_message(Player.chef().id,"Você chutou o banquin de "+p.first+" e ele morreu enforcado.")
                        bot.send_message(Player.chef().id,board(p),parse_mode = "Markdown")
                        bot.send_message(Player.chef().id,"Palavra: "+word["mask"])
                        next_player()
                process()
            else:
                bot.send_message(p.id, "Essa letra já foi usada. Use uma das letras na lista a baixo")
                bot.send_message(p.id, board(p),parse_mode = "Markdown")
                bot.send_message(p.id,"Palavra: "+word["mask"])
                bot.send_message(p.id, "Qual letra você quer?")
        else:
            bot.send_message(p.id, "Ainda não é a sua vez. Aguarde que jaja lhe chamo! Senta lá cláudia!")

bot.polling()