import matplotlib.pyplot as plt

class Plotter:

    def __init__(self,filename="score.png"):
        self.filename = filename
        # self.iteration = 0
        self.iterations = []
        self.scores = []

    def add_result(self,score,number_of_iterations):
        self.scores.append(score)
        if not self.iterations or len(self.iterations) == 0:
            self.iterations.append( number_of_iterations)
        else:
            self.iterations.append(self.iterations[-1] + number_of_iterations)

        plt.figure()
        plt.semilogy(self.iterations, self.scores)
        plt.ylim(self.scores[0], 1.0)

        plt.xlabel('Iterations')
        plt.ylabel('Score (log scale)')

        plt.savefig(self.filename, dpi=300, bbox_inches='tight')
        plt.close()

        # plt.show()