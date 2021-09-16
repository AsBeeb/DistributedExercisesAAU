from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub
import random

class GossipMessage(MessageStub):

    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        # we use a set to keep the "secrets" here
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'


class Gossip(Device):
    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        while True:
            # in each repetition, let us send the ping to one random other device
            message = GossipMessage(self.index(), random.randint(0, self.number_of_devices()), self._secrets)
            
            if self.index() == message.destination:
                print("DONT SEND From: ", self.index(), "To: ", message.destination)
                continue
            print("From: ", self.index(), "To: ", message.destination)

            # we send the message via a "medium"
            self.medium().send(message)

            # in this instance, we also try to receive some messages, there can be multiple, but
            # eventually the medium will return "None"
            ingoing = self.medium().receive()
            if ingoing is None:
                break

            # let's keep some statistics
            self._secrets.add(ingoing.secrets)

            # this call is only used for synchronous networks
            self.medium().wait_for_next_round()

            # the following is your termination condition, but where should it be placed?
            if len(self._secrets) == self.number_of_devices():
                return
        return

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')
