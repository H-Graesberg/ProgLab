from motors import Motors
from zumo_button import ZumoButton


class Motob():
    """Motor object that manifests an interface between a behavior and motor(s)"""

    def __init__(self):

        self.motors = Motors()
        self.value = ""  # nyeste motor anbefaling

    def update(self, recommendation):  # må snakke med arbitrator hvilken form denne parameteren har
        """Mottar ny anbefaling til motoren, legger det i value og gjør det til en operasjon"""
        if self.value != recommendation:
            self.value = recommendation
            self.motors.stop()
        self.operationalize()

    def operationalize(self):
        """konverterer en anbefaling til en eller flere motor instillinger, som sendes til korresponderende motor(er)"""
        if self.value[0] == "F":
            self.motors.forward(0.25, 0.6)
        elif self.value[0] == "B":
            self.motors.backward(0.25, 0.6)
        elif self.value[0] == "L":
            self.motors.left(
                0.5, (int(self.value[1]) * 10 + int(self.value[2])) * 0.01)
        elif self.value[0] == "R":
            self.motors.right(
                0.5, (int(self.value[1]) * 10 + int(self.value[2])) * 0.01)
        elif self.value[0] == "T":
            self.motors.set_value([-1, 1], 0.5)
        elif self.value[0] == "S":
            self.motors.stop()


def main():
    m = Motob()
  #  pdb.set_trace()
    ZumoButton().wait_for_press()
    m.motors.forward(0.25, 5)
    '''
    m.update("F")
    sleep(1)
    m.update("B")
    sleep(1)
    # pdb.set_trace()
    m.update("R90")
    sleep(1)
    print("finished")
    '''

# main()


# a short string or letter to indicate what to do
    # F+20 - (straight) Fremover, svak høyresving
    # F-20 - Fremover, svak venstresving
    # F00 - Rett frem
    # B00 - (back) Rett bakover
    # B+20 - Bakover, svakt til høyre. Fortsetter vinkel som fra S20
    # B-20 - Bakover, svakt til venstre
    # T00 - 180grader rundt, samme som kjøre L180/R180
