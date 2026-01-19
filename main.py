from collections import defaultdict
import random

class KuhnNode():
    def __init__(self,history:str="",cards: tuple =(0,0)):
        self.history=history
        self.cards=cards
        

    @property
    def vez(self):
        return len(self.history)%2
    
    def fim(self):
        return self.history in ["pp","bb","bp","pbp","pbb"]
    
    def aposta(self):
        card_values = {'J': 1, 'Q': 2, 'K': 3}
        heroi=self.cards[0]
        vilao=self.cards[1]
        delta=card_values[heroi]-card_values[vilao]

        if self.history == "bp":
            return 1
        if self.history == "pbp":
            return -1
        if self.history in ("pp", "bb", "pbb"):
            pot_size = 2 if 'b' in self.history else 1
            if delta > 0: 
                return pot_size
            else:
                return -pot_size


    def acao(self):
        if self.fim():
            return []
        else:
            return ["p","b"]

    def proxima_vez(self,escolha):
        return KuhnNode(self.history + escolha, self.cards)
    
    def informacao(self):
        carta=self.cards[self.vez]
        return f"{carta}_{self.history}"
    

class CFRbot():
    def __init__(self,node_class):
        self.node_class=node_class
        self.regret=defaultdict(float)
        self.estrategia=defaultdict(float)
        
    def get_estrategy(self,infoset_key,action):
        positive_regret={acao:max(0,self.regret[f"{infoset_key}_{acao}"]) for acao in range(action)}
        soma_regret=sum(positive_regret.values())
        estrategy={}
        if soma_regret>0:
            estrategy={num:(positive_regret[num]/soma_regret) for num in range(action)}
        else:
            for i in range(action):
                estrategy[i]=1/action
        return estrategy
            
    def cfr(self,node,reach1=float,reach2=float):
        if node.fim():
            return node.aposta()
        
        next_node=node
        
        info=node.informacao()
        jogador_atual=node.vez
        numero_de_jogadas=node.acao()
        probabiidade_escolha=self.get_estrategy(info,len(numero_de_jogadas))
        temp=defaultdict(float)
        lista_acao=node.acao()
        valor_medio=0
        for i,acao in enumerate(lista_acao):
                next_node=node.proxima_vez(acao)

                if jogador_atual==0:
                    temp[i]=-self.cfr(next_node,probabiidade_escolha[i]*reach1,reach2)
                else:
                    temp[i]=-self.cfr(next_node,reach1,probabiidade_escolha[i]*reach2)

                valor_medio+=temp[i]*probabiidade_escolha[i]
        if jogador_atual==0:
            reach=reach2
        else:
            reach=reach1
        for i in range(len(lista_acao)):
            self.regret[f"{info}_{i}"]
            regret=temp[i]-valor_medio
            self.regret[f"{info}_{i}"]+=regret*reach
            if jogador_atual==0:
                self.estrategia[f"{info}_{i}"]+=reach1*probabiidade_escolha[i]
            else:
                self.estrategia[f"{info}_{i}"]+=reach2*probabiidade_escolha[i]
        return valor_medio
    def train(self,numero_de_iteracao):
         deck = ['J', 'Q', 'K']
         for i in range(numero_de_iteracao):
            random.shuffle(deck)

            cartas=tuple(deck[:2])
            
            no=self.node_class(history="", cards=cartas)

            self.cfr(no,1.0,1.0)

    def porcentagem(self):
        avg_strategy = defaultdict()
        deck=["K","Q","J"]
        escolha=["","p","b","pb"]
        for i in deck:
            for j in escolha:
                num2=self.estrategia[f"{i}_{j}_{0}"]

                num1=self.estrategia[f"{i}_{j}_{1}"]

                numt=num1+num2

                if numt==0:
                    avg_strategy[f"{i}_{j}"]=f"{50}%        {50}%"
                else:
                    avg_strategy[f"{i}_{j}"]=f"{((num2/numt)*100):.2f}%    {((num1/numt)*100):.2f}%"

        return dict(sorted(avg_strategy.items()))
if __name__ == "__main__":
    bot = CFRbot(KuhnNode)
    bot.train(150000)
    final_strategy = bot.porcentagem()
    

print(f"Ações: 0='Passar', 1='Apostar'")
print(f"{'Situação'.ljust(10)} -> Estratégia [Passar, Apostar]") # Melhorar o cabeçalho
for infoset, strategy in final_strategy.items():
    print(f"{infoset.ljust(10)} -> {strategy}")