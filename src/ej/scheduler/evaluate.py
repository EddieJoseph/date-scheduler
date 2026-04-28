from ej.scheduler.generation.evaluation.as_clean_evaluator import AsCleanEvaluator
from ej.scheduler.generation.evaluation.assi_evaluator import AssiEvaluator
from ej.scheduler.generation.evaluation.holiday_evaluator import HolidayEvaluator
from ej.scheduler.generation.evaluation.jf_holiday_evaluator import JfHolidayEvaluator
from ej.scheduler.generation.evaluation.month_evaluator import MonthEvaluator
from ej.scheduler.generation.evaluation.same_day_evaluator import SameDayEvaluator
from ej.scheduler.generation.evaluation.type_spread_evaluator import TypeSpreadEvaluator
from ej.scheduler.generation.evaluation.week_clumping_evaluator import WeekClumpingEvaluator
from ej.scheduler.generation.evaluation.week_day_evaluator import WeekDayEvaluator
from ej.scheduler.generation.evaluation.weekend_evaluator import WeekendEvaluator
from ej.scheduler.generation.sampling_data_holder import SamplingDataHolder
from ej.scheduler.util.scheduler_config import SchedulerData


def evaluate_schedule(input_file: str, holidays_file: str, year: int) -> tuple[list[tuple[str, float]], float]:
    type_spread_evaluator = TypeSpreadEvaluator()
    holiday_evaluator = HolidayEvaluator(holidays_file, year)
    jf_holiday_evaluator = JfHolidayEvaluator(holidays_file, year)
    as_evaluator = AsCleanEvaluator(year)
    weekend_evaluator = WeekendEvaluator(year)
    week_clumping_evaluator = WeekClumpingEvaluator(year)
    same_day_evaluator = SameDayEvaluator()
    month_evaluator = MonthEvaluator()
    assi_evaluator = AssiEvaluator()
    week_day_evaluator = WeekDayEvaluator(year)

    evaluators = [
        type_spread_evaluator, holiday_evaluator, jf_holiday_evaluator,
        as_evaluator, weekend_evaluator, week_clumping_evaluator,
        same_day_evaluator, month_evaluator, assi_evaluator, week_day_evaluator,
    ]

    data = SchedulerData.create_from(input_file)
    data_np = SamplingDataHolder(data)

    type_spread_evaluator.set_types(data_np)
    jf_holiday_evaluator.set_jf_type(data_np)
    assi_evaluator.set_assi_types(data_np)
    same_day_evaluator.set_info_type(data_np)
    week_day_evaluator.add_type("KP", data_np)
    week_day_evaluator.add_type("F", data_np)
    week_day_evaluator.add_type("ASI", data_np)

    candidate = data_np.get_np_data()
    scores = [(e.get_name(), e.evaluate(candidate)) for e in evaluators]
    combined = 1.0
    for _, s in scores:
        combined *= s

    _print_results(scores, combined)
    return scores, combined


def _print_results(scores: list[tuple[str, float]], combined: float) -> None:
    name_width = max(len(name) for name, _ in scores)
    for name, score in scores:
        print(f"  {name:<{name_width}}  {score:.6f}")
    print(f"  {'-' * (name_width + 10)}")
    print(f"  {'Combined':<{name_width}}  {combined:.6f}")
