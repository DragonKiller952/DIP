class Computer:
    def __init__(self, id, net, acc=None, lea=None):
        self.id = id
        self.failed = False
        self.network = net
        self.acceptors = acc
        self.learners = lea
        self.prior = False
        self.changed = False #prop
        self.accepted = 0 #prop
        self.rejected = 0 #prop
        self.promise = 0 #prop
        self.consensus = False #prop
        self.initval = None #prop
        self.maxval = None #both
        self.maxID = 0 #acc
        self.matrixes = None
        self.predicted = 0

    def DeliverMessage(self, m):
        #         print('im gonna deliver')
        global proposal
        if m.type == 'PROPOSE':
            proposal +=1
            self.initval = m.value
            self.maxval = m.value
            for i in self.acceptors.keys():
                mn = Message()
                mn.type = 'PREPARE'
                mn.src = m.dst
                mn.dst = i
                mn.value = m.value
                mn.proposalID = proposal
                self.network.Queue_Message(mn)

        elif m.type == 'PREPARE':
            mn = Message()
            mn.type = 'PROMISE'
            mn.src = m.dst
            mn.dst = m.src
            if self.prior:
                mn.value = self.maxval
            else:
                mn.value = m.value
            mn.proposalID = m.proposalID
            self.network.Queue_Message(mn)
        elif m.type == 'PROMISE':
            self.promise += 1
            if self.maxval != m.value and not self.changed:
                self.maxval = m.value
                self.changed = True
            if self.promise == len(self.acceptors.keys()):
                for i in self.acceptors.keys():
                    mn = Message()
                    mn.type = 'ACCEPT'
                    mn.src = m.dst
                    mn.dst = i
                    mn.value = self.maxval
                    mn.proposalID = m.proposalID
                    self.network.Queue_Message(mn)

            # mn = Message()
            # mn.type = 'ACCEPT'
            # mn.src = m.dst
            # mn.dst = m.src
            # mn.value = m.value
            # mn.proposalID = m.proposalID
            #             print(mn.type, mn.src, mn.dst, mn.value)

            # self.network.Queue_Message(mn)
        elif m.type == 'ACCEPT':
            if self.prior:
                if m.proposalID < self.maxID:
                    mn = Message()
                    mn.type = 'REJECTED'
                    mn.src = m.dst
                    mn.dst = m.src
                    mn.value = m.value
                    mn.proposalID = m.proposalID
                    self.network.Queue_Message(mn)
                else:
                    self.maxID = m.proposalID
                    self.maxval = m.value
                    mn = Message()
                    mn.type = 'ACCEPTED'
                    mn.src = m.dst
                    mn.dst = m.src
                    mn.value = m.value
                    mn.proposalID = m.proposalID
                    self.network.Queue_Message(mn)
            else:
                self.prior = True
                self.maxID = m.proposalID
                self.maxval = m.value
                mn = Message()
                mn.type = 'ACCEPTED'
                mn.src = m.dst
                mn.dst = m.src
                mn.value = m.value
                mn.proposalID = m.proposalID
                self.network.Queue_Message(mn)
        elif m.type == 'SUCCESS':
            if not self.matrixes:
                matrixnl = {i: {j: 0 for j in 'abcdefghijklmnopqrstuvwxyz $'} for i in
                                 'abcdefghijklmnopqrstuvwxyz $'}
                matrixen = {i: {j: 0 for j in 'abcdefghijklmnopqrstuvwxyz $'} for i in
                                 'abcdefghijklmnopqrstuvwxyz $'}
                self.matrixes = {'nl': matrixnl, 'en': matrixen}
            value = m.value
            value = value.split(':')
            if len(value[1]) < 2:
                value[1] += ' '
            self.matrixes[value[0]][value[1][0]][value[1][1]] += 1
            self.predicted += 1
            for i in self.acceptors.keys():
                self.acceptors[i].maxID = 0
                self.acceptors[i].maxval = None
                self.acceptors[i].prior = False
            proposal = 0
            mn = Message()
            mn.type = 'PREDICTED'
            mn.src = m.dst
            mn.dst = None
            mn.value = None
            mn.proposalID = self.predicted
            self.network.Queue_Message(mn)


        else:
            if m.type == 'ACCEPTED':
                self.accepted += 1
            else:
                self.rejected += 1
            if self.accepted + self.rejected == len(self.acceptors.keys()):
                if self.accepted > self.rejected:
                    self.changed = False
                    self.accepted = 0
                    self.rejected = 0
                    self.promise = 0
                    self.consensus = True
                    for i in self.learners.keys():
                        mn = Message()
                        mn.type = 'SUCCESS'
                        mn.src = m.dst
                        mn.dst = i
                        mn.value = m.value
                        mn.proposalID = m.proposalID
                        self.network.Queue_Message(mn)
                else:
                    proposal += 1
                    self.changed = False
                    self.accepted = 0
                    self.rejected = 0
                    self.promise = 0
                    self.maxval = m.value
                    for i in self.acceptors.keys():
                        mn = Message()
                        mn.type = 'PREPARE'
                        mn.src = m.dst
                        mn.dst = i
                        mn.value = m.value
                        mn.proposalID = proposal
                        self.network.Queue_Message(mn)


class Message:
    def __init__(self):
        self.src = None
        self.dst = None
        self.type = None
        self.value = None
        self.proposalID = None


class Network:
    def __init__(self):
        self.queue = []
        self.proposers = None
        self.acceptors = None

    def Queue_Message(self, m):
        self.queue.append(m)

    def Extract_Message(self):
        for m in self.queue:
            if 'L' in m.src or 'L' in m.dst:
                self.queue.remove(m)
                return m
            elif 'P' in m.src:
                if self.proposers[m.src].failed == False and self.acceptors[m.dst].failed == False:
                    self.queue.remove(m)
                    return m
            else:
                if self.acceptors[m.src].failed == False and self.proposers[m.dst].failed == False:
                    self.queue.remove(m)
                    return m
        return None


def Simulate(n_p, n_a, n_l,tmax, E):
    ticklen = len(str(tmax))
    finished = False
    #   /* Initializeer Proposer and Acceptor sets, maak netwerk aan*/
    N = Network()
    A = {'A' + str((i + 1)): Computer('A' + str((i + 1)), N) for i in range(n_a)}
    L = {'L' + str((i + 1)): Computer('L' + str((i + 1)), N, A) for i in range(n_l)}
    P = {'P' + str((i + 1)): Computer('P' + str((i + 1)), N, A, L) for i in range(n_p)}
    N.proposers = P
    N.acceptors = A
    N.learners = L
    #     comps = P+A
    global proposal
    proposal = 0

    for t in range(0, tmax):
        #         print(len(E))
        #         print(len(N.queue) == 0 or len(E) == 0)
        if len(N.queue) == 0 and len(E) == 0:
            #             print('empty')
            # Als er geen berichten of zijn of events, dan is de simulatie afgelopen.
            if not finished:
                print()
                for key in P.keys():
                    if P[key].consensus:
                        print('{} heeft wel consensus (voorgesteld: {}, geaccepteerd: {})'.format(key, P[key].initval,
                                                                                                  P[key].maxval))
                    else:
                        print('{} heeft geen consensus.'.format(key))
            return
        # Verwerk event e (als dat tenminste bestaat)
        e = [i for i in E if i[0] == t]
        e = None if e == [] else e[0]
        if e is not None:
            E.remove(e)
            #             print(e)
            (t, F, R, pi_c, pi_v) = e
            #             print((t, F, R, pi_c, pi_v))
            for c in F:
                print('{}: ** {} kapot **'.format('%03d' % t, c))
                if 'P' in c:
                    P[c].failed = True
                else:
                    A[c].failed = True
            for c in R:
                print('{}: ** {} gerepareerd **'.format('%03d' % t, c))
                if 'P' in c:
                    P[c].failed = False
                else:
                    A[c].failed = False
            if pi_v is not None and pi_c is not None:
                finished = False
                m = Message()
                m.type = 'PROPOSE'
                m.src = None  # PROPOSE-bericht beginnen buiten het netwerk.
                m.dst = pi_c
                m.value = pi_v
                print('{}:    -> {}  PROPOSE v={}'.format('%03d' % t, m.dst, m.value))
                P[pi_c].DeliverMessage(m)
        else:
            m = N.Extract_Message()
            if m is not None:
                #                 if m.type = 'PROPOSE':
                #                     print('{}:    -> P{}  PROPOSE v={}'.format(t, m.dst, m.value))
                if m.type == 'PREPARE':
                    print('{}: {} -> {}  PREPARE n={}'.format('%03d' % t, m.src, m.dst, m.proposalID))
                    A[m.dst].DeliverMessage(m)
                elif m.type == 'PROMISE':
                    if A[m.src].prior:
                        print('{}: {} -> {}  PROMISE n={} (Prior: n={}, v={})'.format('%03d' % t, m.src, m.dst,
                                                                                      m.proposalID, A[m.src].maxID,
                                                                                      A[m.src].maxval))
                    else:
                        print('{}: {} -> {}  PROMISE n={} (Prior: None)'.format('%03d' % t, m.src, m.dst, m.proposalID))
                    P[m.dst].DeliverMessage(m)
                elif m.type == 'ACCEPT':
                    print('{}: {} -> {}  ACCEPT n={} v={}'.format('%03d' % t, m.src, m.dst, m.proposalID, m.value))
                    A[m.dst].DeliverMessage(m)
                elif m.type == 'ACCEPTED':
                    print('{}: {} -> {}  ACCEPTED n={} v={}'.format('%03d' % t, m.src, m.dst, m.proposalID, m.value))
                    P[m.dst].DeliverMessage(m)
                elif m.type == 'REJECTED':
                    print('{}: {} -> {}  REJECTED n={}'.format('%03d' % t, m.src, m.dst, m.proposalID))
                    P[m.dst].DeliverMessage(m)
            #                 if m.type in ['PREPARE', 'ACCEPT']:
            #                     A[m.dst].DeliverMessage(m)
            #                 else:
            #                     P[m.dst].DeliverMessage(m)
            #                 DeliverMessage(m.dst, m)
                elif m.type == 'SUCCESS':
                    print('{}: {} -> {}  SUCCESS n={} v={}'.format('%03d' % t, m.src, m.dst, m.proposalID, m.value))
                    L[m.dst].DeliverMessage(m)
                elif m.type == 'PREDICTED':
                    finished = True
                    print('{}: {} ->     PREDICTED n={}'.format('%03d' % t, m.src, m.proposalID))
                    print()
                    for key in P.keys():
                        print('{} heeft wel consensus (voorgesteld: {}, geaccepteerd: {})'.format(key, P[key].initval,
                                                                                                  P[key].maxval))
                        P[key].consensus = False
                        P[key].initval = None
                        P[key].maxval = None
                    print()
            else:
                print('{}:'.format('%03d' % t))

    for key in P.keys():
        if P[key].consensus:
            print('{} heeft wel consensus (voorgesteld: {}, geaccepteerd: {})'.format(key, P[key].initval,
                                                                                      P[key].maxval))
        else:
            print('{} heeft geen consensus.'.format(key))



def main(file):
    file = open(file, 'r')
    file = file.read().splitlines()

    start = file[0].split(' ')
    file = file[1:-1]
    n_p = int(start[0])
    n_a = int(start[1])
    n_l = int(start[2])
    tmax = int(start[3])
    #     print(file)
    E = []

    current = None
    for i in file:
        i = i.split(' ')
        if current == None:
            current = [int(i[0]), [], [], None, None]
        if int(i[0]) != current[0]:
            E.append(current)
            current = [int(i[0]), [], [], None, None]

        if 'FAIL' in i:
            if 'PROPOSER' in i:
                current[1].append('P{}'.format(i[-1]))
            else:
                current[1].append('A{}'.format(i[-1]))
        elif 'RECOVER' in i:
            if 'PROPOSER' in i:
                current[2].append('P{}'.format(i[-1]))
            else:
                current[2].append('A{}'.format(i[-1]))
        elif 'PROPOSE' in i:
            current[3] = 'P' + i[2]
            current[4] = ' '.join(i).split(' {} '.format(i[2]))[-1]
    E.append(current)
    #     print(E)

    Simulate(n_p, n_a, n_l, tmax, E)

main('inputLearn.txt')
