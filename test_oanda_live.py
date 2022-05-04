from Services.Assistant import Assistant
from Brokers import OandaBroker, Qu4ntBroker
from Strategies import EngulfingStrategy
from Args import ArgsLive, ArgsBacktest
from Domain.Enum import PositionType
from Domain.Enum import OrderType
from Domain.Enum import InstrumentType

args_qu4nt = ArgsBacktest()
args_oanda = ArgsLive()

broker = OandaBroker(args_oanda)
# broker = Qu4ntBroker(args_qu4nt)
broker.trade_manager.close_all_trade()

result, response = broker.market_order_request(
    InstrumentType.eurusd.value,
    -1000
)
print(result, response)
if result:
    broker.take_profit_order_request(response, 50)
    broker.stop_loss_order_request(response, 15)









# broker.trade_manager.close_all_trade()














# position_type = PositionType.SHORT
# if position_type is PositionType.LONG:
#     units = strategy.sizer.calc_units(
#         broker.account.get_margin_available(),
#         broker.account.get_leverage(),
#         broker.pricing.get_current_ask(),
#     )
# elif position_type is PositionType.SHORT:
#     units = -strategy.sizer.calc_units(
#         broker.account.get_margin_available(),
#         broker.account.get_leverage(),
#         broker.pricing.get_current_bid(),
#     )
#
# order_market_request = OrderMarketRequestModel(
#     OrderType.MARKET,
#     position_type,
#     units
# )
# # Assistant.print_object(order_market_request)
# result, market_order = broker.create_order(order_market_request)
#
# print(result)
#
# broker.trade_manager.get_open_trade()
#
# # orders.append(market_order)



