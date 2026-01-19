from collections import defaultdict
import random
class CFRbot():
    def __init__(self,node_class):
        self.node_class=node_class
        self.regret=defaultdict(float)
        self.estrategia=defaultdict(float)
        
    def get_estrategy(self,infoset_key,action):
        self.positive_regret={acao:max(0,self.regret[f"{infoset_key}_{acao}"]) for acao in range(action)}
        soma_regret=sum(self.positive_regret.values())
        estrategy={}
        if soma_regret>0:
            estrategy={num:(self.positive_regret[num]/soma_regret) for num in range(action)}
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
        probabiidade_escolha=self.get_estrategy(info,numero_de_jogadas)
        temp=defaultdict(float)
        lista_acao=node.acao()
        valor_medio=0
        for i,acao in enumerate(lista_acao):
                next_node=node.proxima_vez(acao)

                if jogador_atual==0:
                    temp[i]=self.cfr(next_node,probabiidade_escolha[i]*reach1,reach2)
                else:
                    temp[i]=self.cfr(next_node,reach1,probabiidade_escolha[i]*reach2)

                valor_medio+=temp[i]*probabiidade_escolha[i]
        if jogador_atual==0:
            reach=reach2
        else:
            reach=reach1
        for i in range(len(lista_acao)):
            self.regret[f"{info}_{i}"]
            regret=temp[i]-valor_medio
            self.regret[f"{info}_{i}"]=regret*reach
            if jogador_atual==0:
                self.estrategia[f"{info}_{i}"]=reach1*probabiidade_escolha[i]
            else:
                self.estrategia[f"{info}_{i}"]=reach2*probabiidade_escolha[i]
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
        deck=["k","Q","J"]
        escolha=["","p","b","pb"]
        for i in deck:
            for j in escolha:
                num1=self.estrategia[f"{i}_{j}_{0}"]

                num2=self.estrategia[f"{i}_{j}_{1}"]

                numt=num1+num2

                avg_strategy[f"{i}_{j}"]=f"{(num1/numt):.2f}%{(num2/numt):.2f}%"

        return dict(sorted(avg_strategy.items()))
if __name__ == "__main__":
    bot = CFRbot()
    bot.train(100000)
    final_strategy = bot.get_average_strategy()
    
    print("\n--- ESTRATÉGIA FINAL APRENDIDA ---")
    print(f"Ações: 0='Passar', 1='Apostar'")
    for infoset, strategy in final_strategy.items():
        print(f"Situação: {infoset.ljust(6)} -> Estratégia [P, B]: {strategy}")