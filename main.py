from Args import ArgsBacktest
from Args import ArgsLive
from Containers.Processors import ContainerProcessors
from Domain.Enum import ProcessorType
from Services.DrawPlot import DrawPlot
from Services.Assistant import Assistant
from Services.OutcomesManager import OutcomesManager

args = ArgsBacktest()
# args = ArgsLive()

containerProcessors = ContainerProcessors()
if args.parameters.processor_type == ProcessorType.backtest:
    processor = containerProcessors.backtest_processor_provider(args=args)
    processor.run()
    DrawPlot(processor)
    outcomes_manager = OutcomesManager(
        args,
        processor.broker.pricing.data_main,
        processor.broker.pricing.data_stream,
        processor.broker.outcomes,
    )
    outcomes_manager.print_outcomes()
elif args.parameters.processor_type == ProcessorType.live:
    processor = containerProcessors.live_processor_provider(args=args)
else:
    print("Error")
    exit()
