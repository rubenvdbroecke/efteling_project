# this class gets a permutation and a time limit, it attempts to crash optimally.

import random
import read_data
import time

if __name__ == '__main__':
    def run():
        dataclass = read_data.DataClass()
        attracties = [16, 23, 20, 18, 6, 22, 5, 13, 9]
        pso = PSO_attempt()
        time1 = time.time()
        tradeoffprice = 20000
        startinghour = 84
        deadline = 117
        startinglocation = 6
        pso.crashPermutation(attracties, 1000, 20, 0.729, 2.025, 2.025, dataclass.averagewaitingtimes,
                             dataclass.lengthofevents, dataclass.distancetimes, deadline, startinghour,
                             startinglocation, tradeoffprice, dataclass.indextable)
        print(time.time() - time1)


class PSO_attempt:
    def crashPermutation(self, permutation, swarmsize, generations, omega, phip, phig, wachttijdentable, duurtijdtable,
                         afstandtable, deadline, startingtime, startingposition, tradeoff, indextable):
        # enkel length of permutation is hier eigelijk belangrijk.


        swarm = []
        permlen = len(permutation)
        for fly in range(swarmsize):
            choices = []
            for i in range(len(permutation)):
                choices.append(random.uniform(0.0, 4.0))
            swarm.append(choices)

        bestknownposition = []
        bestknownscores = []
        bestscoreever = 100000

        for i in swarm:
            bestknownposition.append(i)
            bestknownscores.append(
                self.evaluate(i, wachttijdentable, duurtijdtable, afstandtable, permutation, deadline, startingtime,
                              startingposition, tradeoff, indextable))
        bestknownpos = swarm[0]

        v = []
        for i in range(len(swarm)):
            speed = []
            for j in range(len(permutation)):
                speed.append(random.uniform(-4.0, 4.0))
            v.append(speed)

        for i in range(generations):
            for particle in range(swarmsize):
                for d in range(permlen):
                    rp = random.uniform(0, 1)
                    rg = random.uniform(0, 1)
                    # update velocity

                    v[particle][d] = omega * v[particle][d] + phip * rp \
                                                              * (bestknownposition[particle][d] - swarm[particle][
                        d]) + phig * rg * (bestknownpos[d] - swarm[particle][d])
                    # update position
                    newpos = swarm[particle][d] + v[particle][d]
                    if newpos >= 0.0:
                        swarm[particle][d] = newpos
                        if newpos <= 4.0:
                            swarm[particle][d] = newpos
                        else:
                            swarm[particle][d] = 4.0
                    else:
                        swarm[particle][d] = 0.0
                score = self.evaluate(swarm[particle], wachttijdentable, duurtijdtable, afstandtable, permutation,
                                      deadline, startingtime, startingposition, tradeoff, indextable)

                if score < bestknownscores[particle]:
                    bestknownscores[particle] = score
                    bestknownposition[particle] = swarm[particle]
                    # print(score)
                if score < bestscoreever:
                    bestscoreever = score
                    bestknownpos = swarm[particle]
                    # print(score)
                    # print(bestknownscores)
        print(bestscoreever, 'runner ups', bestknownscores)
        self.evaluate(bestknownpos, wachttijdentable, duurtijdtable, afstandtable, permutation, deadline,
                      startingtime, startingposition, tradeoff, indextable)

    def evaluate(self, particle, wachttijdentable, duurtijdtable, afstandtable, permutatie, deadline, startingtime,
                 startingposition, tradeoff, indextable):  # returns cost! not in time -> big penalty
        # print('evaluate')
        decisions = []
        for sc in particle:
            decisions.append(int(round(sc)))
        leng = len(permutatie)
        timenow = startingtime
        totalcost = 0
        vorige = startingposition
        missed = 0
        for i in range(leng):
            print(str(getTime(timenow)), ': wandel ', str(afstandtable[vorige][permutatie[i]]), ' minuten')
            timenow += afstandtable[vorige][permutatie[i]] / 5

            percAndCost = self.getPercentageAndFixedCost(decisions[i])
            if percAndCost[0] == 1.0:
                # no waiting time
                totalcost += percAndCost[1]
                pass
            else:
                if timenow > 117:
                    print('park closed')
                    waitingtime = 0
                else:
                    waitingtime = wachttijdentable[permutatie[i]][int(round(timenow))] / 5
                    print(str(getTime(timenow)), ': wacht ',
                          str(wachttijdentable[permutatie[i]][int(round(timenow))] * (1 - percAndCost[0])),
                          ' minuten   ', end="")
                    timenow += waitingtime * (1 - percAndCost[0])
                if percAndCost[0] > 0.0:
                    totalcost += percAndCost[1] + 0.06 * waitingtime * (1 - percAndCost[0])
            ######

            if percAndCost[0] == 0.0:
                print('Do not crash')
            elif percAndCost[0] == 0.3:
                print('Bronze')
            elif percAndCost[0] == 0.5:
                print('Silver')
            elif percAndCost[0] == 0.9:
                print('Gold')
            elif percAndCost[0] == 1.0:
                print(getTime(timenow), ':single shot')

            ######
            if timenow > deadline:

                line = ': missed '
                missed += 1
            else:
                line = ': joepie! '
            print(
            str(getTime(timenow)), line, str(round(duurtijdtable[permutatie[i]] / 60, 2)), ' minuten leute op de ',
            indextable[permutatie[i]])
            timenow += duurtijdtable[permutatie[i]] / 300

            vorige = permutatie[i]

        totalcost += missed * tradeoff
        print("missed", missed, 'Deadline:', getTime(deadline))
        print('actual cost', totalcost - missed * tradeoff)

        return totalcost

    def getPercentageAndFixedCost(self, decision):
        if decision == 0:
            return [0.0, 1]
        if decision == 1:
            return [0.3, 0.5]
        if decision == 2:
            return [0.5, 1.25]
        if decision == 3:
            return [0.9, 2.0]
        if decision == 4:
            return [1.0, 5]


class crash:
    def crashPermutation(self, permutation, startuur, deadline):
        # crash price =  fixed(type) + f(wachtrij)

        # what this method does, is go look at the waiting times, see what methods can win enough time to catch
        # the deadline, and takes the cheapest one. Does it check all options?


        benefitbronze = 0.3
        benefitsilver = 0.5
        benefitgold = 0.9

        fixedbronze = 0.5
        fixedsilver = 1.25
        fixedgold = 2.0
        fixedsingleshot = 5.0

        priceperminute = 0.06

        # price = fixed + priceperminute * benefit * waitingtime

        # how many options ? pow(4,len(perm))     = 1 000 000 for 10 attr.
        # check all? Is there a better heuristic? Well, cost increases are not entirely linear
        # Try cheapest option every time, and if it's not sufficient.
        #
        # why not try particle swarm optimization?



        """
        n walibi werken ze met een systeem met verschillende gradaties van voorsteken. vb:
        brons -> 30% minder wachten.
        zilver 50% wachten.
        Gold -> 90% minder wachten.
        single shot -> geen wachtrij

        """


def getTime(uur):
    achtdertig = 102 * 5
    minutentijd = uur * 5
    totalhourinminutes = achtdertig + minutentijd
    hour = totalhourinminutes // 60
    minutes = totalhourinminutes % 60
    if len(str(int(minutes))) == 1:
        minutes = '0' + str(int(minutes))
    else:
        minutes = str(int(minutes))
    return ''.join([str(int(hour)), 'h', minutes])


if __name__ == "__main__":
    run()
