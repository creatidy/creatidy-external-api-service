import grpc
from concurrent import futures
import time
import datetime
import decimal

# import the generated classes
import protobufs.currency_rates_pb2
import protobufs.currency_rates_pb2_grpc

# import the original calculator.py
from source_controller.currency_rates import FiatCurrencyRates


class RatesServicer(protobufs.currency_rates_pb2_grpc.RatesServicer):

    def GetRate(self, request, context):
        sell = request.sell
        date = datetime.datetime.fromtimestamp(request.timestamp.seconds)
        response = protobufs.currency_rates_pb2.Rate()
        fiat = FiatCurrencyRates()
        rate = fiat.get_rate_pln(sell, date)
        response.value = float(rate)
        return response

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
protobufs.currency_rates_pb2_grpc.add_RatesServicer_to_server(RatesServicer(), server)

# listen on port 50052
print('Starting server. Listening on port 50052.')
server.add_insecure_port('[::]:50052')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
