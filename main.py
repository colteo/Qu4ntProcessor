from Args import ArgsBacktest
from Args import ArgsLive
from Domain.Enum import ProcessorType
from Services.DrawPlot import DrawPlot
from Services.Assistant import Assistant
from Services.OutcomesManager import OutcomesManager
from Processors import BacktestProcessor, LiveProcessor

args = ArgsBacktest()
# args = ArgsLive()

if args.parameters.processor_type == ProcessorType.backtest:
    processor = BacktestProcessor(args=args)
    processor.run()
    DrawPlot(processor)
    outcomes_manager = OutcomesManager(
        args,
        processor.broker.pricing.data_main,
        processor.broker.pricing.data_stream,
        processor.broker.outcomes,
    )

elif args.parameters.processor_type == ProcessorType.live:
    processor = LiveProcessor(args=args)
else:
    print("Error")
    exit()
