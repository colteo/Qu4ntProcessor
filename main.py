from Args import Args
from Domain.Enum import ProcessorType
from Services.DrawPlot import DrawPlot
from Services.Assistant import Assistant
from Services.OutcomesManager import OutcomesManager
from Processors import BacktestProcessor, LiveProcessor

args = Args()

if args.parameters.processor_type == ProcessorType.backtest:
    processor = BacktestProcessor(args=args)
    processor.run()
    # DrawPlot(processor)
    outcomes_manager = OutcomesManager(
        args,
        processor,
        print_html=True,
        send_result_to_server_api=True
    )

elif args.parameters.processor_type == ProcessorType.live:
    processor = LiveProcessor(args=args)
    processor.run()
else:
    print("Error")
    exit()
