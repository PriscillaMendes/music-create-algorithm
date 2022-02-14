from mido import MidiFile
from mido import Message, MidiFile, MidiTrack
import numpy as np

mid = MidiFile('MIDI/VampireKillerCV1.mid', clip=True)
print(mid)

notaAnterior = -1
maiorNota = -1
menorNota = 1000
maiorVelocidade = -1
velocidadeAnterior = -1
menorVelocidade = 1000000
tabelaTransicao = np.zeros((100,100), dtype=np.float64)
tabelaTransicaoVelocidade = np.zeros((100,100), dtype=np.float64)
tabelaTransicaoTempo = {}
tbTransicaoTempo = {}

tempoAnterior = -1
for track in mid.tracks:
    for msg in track:
        if(msg.type == 'note_on'):
            if(msg.note < menorNota):
                menorNota = msg.note
            if notaAnterior < 0:
                notaAnterior = msg.note
            if tempoAnterior < 0:
                tempoAnterior = msg.time

            if (msg.note < menorNota):
                menorNota = msg.note

            else:
                tabelaTransicao[notaAnterior][msg.note] += 1
                notaAnterior = msg.note
                if((tempoAnterior, msg.time) in tbTransicaoTempo):
                    tabelaTransicaoTempo[msg.time] += 1
                    tbTransicaoTempo[(tempoAnterior, msg.time)] += 1
                    tempoAnterior = msg.time
                else:
                    tabelaTransicaoTempo.update({msg.time: 1})
                    tbTransicaoTempo.update({(tempoAnterior,msg.time): 1})
                    tempoAnterior = msg.time

tbTempo = {}
count = 0
tbTransicaoTempo[(0,0)] = tbTransicaoTempo[(0,0)]/2

for key in tbTransicaoTempo.keys():
    if(key[0] not in tbTempo):
        tbTempo.update({key[0]:count})
        count+=1
    if (key[1] not in tbTempo):
        tbTempo.update({key[1]: count})
        count += 1

tbTransicaoTempoB = np.zeros((count,count), dtype=np.float64)
for key, value in tbTransicaoTempo.items():
    i = tbTempo[key[0]]
    j = tbTempo[key[1]]
    tbTransicaoTempoB[i][j] = value

print(tbTransicaoTempoB)


tbTransicaoTempo = tbTransicaoTempoB
emptyLines = []
for i,linha in enumerate(tbTransicaoTempo):
    if (np.sum(linha) == 0):
        emptyLines.append(i)
    else:
        print("Valor:")
        somadalinha = np.sum(tbTransicaoTempoB[i])
        for j,valor in enumerate(linha):
            valor = valor / somadalinha
            tbTransicaoTempo[i][j] = valor
            print(tbTransicaoTempo[i][j])

tbTransicaoTempo = np.delete(tbTransicaoTempo,emptyLines,axis=0)
tbTransicaoTempo = np.delete(tbTransicaoTempo,emptyLines,axis=1)


estadoInicialtempo = 15
num_notas = 100
tempoSequencia = []
tempoSequencia2 = []

tempo = np.arange(count)

x_p = [estadoInicialtempo]
for i in range(num_notas):
    step = np.random.choice(tempo,p=tbTransicaoTempo[x_p[-1]])
    x_p.append(step)
tempoSequencia = x_p

x_p = [estadoInicialtempo]
for i in range(num_notas):
    step = np.random.choice(tempo,p=tbTransicaoTempo[x_p[-1]])
    x_p.append(step)
tempoSequencia2 = x_p

################ Tabela das Notas

tabelaTransicaoB = tabelaTransicao
emptyLines = []
for i,linha in enumerate(tabelaTransicaoB):
    if (np.sum(linha) == 0):
        emptyLines.append(i)
    else:
        print("Valor:")
        somadalinha = np.sum(tabelaTransicao[i])
        for j,valor in enumerate(linha):
            valor = valor / somadalinha
            tabelaTransicaoB[i][j] = valor
            print(tabelaTransicaoB[i][j])

tabelaTransicaoB = np.delete(tabelaTransicaoB,emptyLines,axis=0)
tabelaTransicaoB = np.delete(tabelaTransicaoB,emptyLines,axis=1)

estadoInicial = 21
num_notas = 100
notasSequencia = []
p = tabelaTransicaoB
n = num_notas
notas = np.arange(22)
notasSequencia = []
print(notas)
x_p = [estadoInicial]
for i in range(n):
    step = np.random.choice(notas,p=tabelaTransicaoB[x_p[-1]])
    x_p.append(step)
notasSequencia = x_p
print(notasSequencia)

#############

arr = np.arange(100)
intervalos = []
for nota in arr:
    if (nota not in emptyLines):
        intervalos.append(nota)

##############

############# Baixo
################ Tabela das Notas
tabelaTransicaoBaixo =  np.linalg.matrix_power(tabelaTransicao, 3)
tabelaTransicaoBaixoB = tabelaTransicaoBaixo
emptyLines = []
for i,linha in enumerate(tabelaTransicaoBaixoB):
    if (np.sum(linha) == 0):
        emptyLines.append(i)
    else:
        print("Valor:")
        somadalinha = np.sum(tabelaTransicaoBaixo[i])
        for j,valor in enumerate(linha):
            valor = valor / somadalinha
            tabelaTransicaoBaixoB[i][j] = valor
            print(tabelaTransicaoBaixoB[i][j])

tabelaTransicaoBaixoB = np.delete(tabelaTransicaoBaixoB,emptyLines,axis=0)
tabelaTransicaoBaixoB = np.delete(tabelaTransicaoBaixoB,emptyLines,axis=1)

estadoInicialBaixo = 10
notasBaixoSequencia = []
p = tabelaTransicaoB
notasBaixo = np.arange(22)
notasBaixoSequencia = []
print(notas)
x_p = [estadoInicialBaixo]
for i in range(n):
    step = np.random.choice(notasBaixo,p=tabelaTransicaoBaixoB[x_p[-1]])
    x_p.append(step)
notasBaixoSequencia = x_p
print("BAIXOOO")
print(notasBaixoSequencia)

#############

my_midi = MidiFile()
my_track = MidiTrack()
my_track_baixo = MidiTrack()

my_midi.tracks.append(my_track)
my_midi.tracks.append(my_track_baixo)

my_track.append(Message('program_change', program=12, time=0))
my_track_baixo.append(Message('program_change', program=12, time=0))

for i in range(num_notas):
    nota = notasSequencia[i]
    nota_baixo = notasSequencia[i]
    for key, value in tbTempo.items():
        if (value == tempoSequencia[i]):
            tempo = key
        if (value == tempoSequencia2[i]):
            tempobaixo = key


    my_track.append(Message('note_on', note=intervalos[nota], velocity=64, time=tempo))
    my_track.append(Message('note_off', note=intervalos[nota], velocity=127, time=tempo))
    my_track_baixo.append(Message('note_on', note=intervalos[nota_baixo]-24, velocity=64, time=tempobaixo))
    my_track_baixo.append(Message('note_off', note=intervalos[nota_baixo]-24, velocity=127, time=tempobaixo))
    i+=1
    if (i == num_notas-1):
        i = 0


my_midi.save('teste.mid')

