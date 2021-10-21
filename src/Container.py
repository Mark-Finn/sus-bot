from dependency_injector import containers, providers

from Domain.Gateway.GameModelGateway import GameModelGateway
from Domain.Gateway.Settings.Gateway import Gateway as SettingsGateway
from Domain.Gateway.Tasks.Gateway import Gateway as TaskGateway
from Domain.UseCase.NewGame.UseCase import UseCase as NewGameUseCase
from Domain.UseCase.JoinColorOptions.UseCase import UseCase as JoinColorOptionsUseCase
from Domain.UseCase.JoinGame.UseCase import UseCase as JoinGameUseCase
from Domain.UseCase.LeaveGame.UseCase import UseCase as LeaveGameUseCase
from Domain.UseCase.GetTasks.UseCase import UseCase as GetTasksUseCase
from Domain.UseCase.GetSettings.UseCase import UseCase as GetSettingsUseCase
from Domain.UseCase.ChangeSetting.UseCase import UseCase as ChangeSettingUseCase
from Domain.UseCase.StartGame.UseCase import UseCase as StartGameUseCase
from Domain.UseCase.TaskCompletion.UseCase import UseCase as TaskCompletionUseCase
from Domain.UseCase.KillOptions.UseCase import UseCase as KillOptionsUseCase
from Domain.UseCase.KillPlayer.UseCase import UseCase as KillPlayerUseCase
from Domain.UseCase.EndGame.UseCase import UseCase as EndGameUseCase
from Domain.UseCase.EmergencyMeeting.UseCase import UseCase as EmergencyMeetingUseCase
from Domain.UseCase.JoinMeeting.UseCase import UseCase as JoinMeetingUseCase
from Domain.UseCase.Meeting.UseCase import UseCase as MeetingUseCase
from Domain.UseCase.Vote.UseCase import UseCase as VoteUseCase
from Domain.UseCase.StartRound.UseCase import UseCase as StartRoundUseCase
from Domain.UseCase.ReportOptions.UseCase import UseCase as ReportOptionsUseCase
from Domain.UseCase.ReportBody.UseCase import UseCase as ReportBodyUseCase
from Domain.UseCase.TaskOptions.UseCase import UseCase as TaskOptionsUseCase
from Domain.UseCase.CompleteTask.UseCase import UseCase as CompleteTaskUseCase
from Domain.UseCase.ReactorSabotage.UseCase import UseCase as ReactorSabotageUseCase
from Domain.UseCase.PressReactorButton.UseCase import UseCase as PressReactorButtonUseCase
from Domain.UseCase.CanSabotage.UseCase import UseCase as CanSabotageUseCase
from Domain.UseCase.ElectricalSabotage.UseCase import UseCase as ElectricalSabotageUseCase
from Domain.UseCase.O2Sabotage.UseCase import UseCase as O2SabotageUseCase
from Domain.UseCase.FlipSwitch.UseCase import UseCase as FlipSwitchUseCase
from Domain.UseCase.EnterCode.UseCase import UseCase as EnterCodeUseCase
from Domain.UseCase.ComSabotage.UseCase import UseCase as ComSabotageUseCase
from Domain.UseCase.RotateKnob.UseCase import UseCase as RotateKnobUseCase


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    # Gateways

    game_model_gateway = providers.Singleton(
        GameModelGateway
    )

    settings_gateway = providers.Singleton(
        SettingsGateway
    )

    task_gateway = providers.Singleton(
        TaskGateway
    )

    # UseCases

    new_game_use_case = providers.Singleton(
        NewGameUseCase,
        game_model_gateway=game_model_gateway,
        settings_gateway=settings_gateway,
        task_gateway=task_gateway
    )

    join_color_options_use_case = providers.Singleton(
        JoinColorOptionsUseCase,
        game_model_gateway=game_model_gateway,
    )

    join_game_use_case = providers.Singleton(
        JoinGameUseCase,
        game_model_gateway=game_model_gateway,
    )

    leave_game_use_case = providers.Singleton(
        LeaveGameUseCase,
        game_model_gateway=game_model_gateway,
    )

    get_tasks_use_case = providers.Singleton(
        GetTasksUseCase,
        game_model_gateway=game_model_gateway,
        task_gateway=task_gateway,
    )

    get_settings_use_case = providers.Singleton(
        GetSettingsUseCase,
        game_model_gateway=game_model_gateway,
        settings_gateway=settings_gateway,
    )

    change_setting_use_case = providers.Singleton(
        ChangeSettingUseCase,
        game_model_gateway=game_model_gateway,
        settings_gateway=settings_gateway,
    )

    start_game_use_case = providers.Singleton(
        StartGameUseCase,
        game_model_gateway=game_model_gateway,
    )

    task_completion_use_case = providers.Singleton(
        TaskCompletionUseCase,
        game_model_gateway=game_model_gateway,
    )

    kill_options_use_case = providers.Singleton(
        KillOptionsUseCase,
        game_model_gateway=game_model_gateway,
    )

    kill_player_use_case = providers.Singleton(
        KillPlayerUseCase,
        game_model_gateway=game_model_gateway,
    )

    end_game_use_case = providers.Singleton(
        EndGameUseCase,
        game_model_gateway=game_model_gateway,
    )

    emergency_meeting_use_case = providers.Singleton(
        EmergencyMeetingUseCase,
        game_model_gateway=game_model_gateway,
    )

    join_meeting_use_case = providers.Singleton(
        JoinMeetingUseCase,
        game_model_gateway=game_model_gateway,
    )

    meeting_use_case = providers.Singleton(
        MeetingUseCase,
        game_model_gateway=game_model_gateway,
    )

    vote_use_case = providers.Singleton(
        VoteUseCase,
        game_model_gateway=game_model_gateway,
    )

    start_round_use_case = providers.Singleton(
        StartRoundUseCase,
        game_model_gateway=game_model_gateway,
    )

    report_options_use_case = providers.Singleton(
        ReportOptionsUseCase,
        game_model_gateway=game_model_gateway,
    )

    report_body_use_case = providers.Singleton(
        ReportBodyUseCase,
        game_model_gateway=game_model_gateway,
    )

    task_options_use_case = providers.Singleton(
        TaskOptionsUseCase,
        game_model_gateway=game_model_gateway,
    )

    complete_task_use_case = providers.Singleton(
        CompleteTaskUseCase,
        game_model_gateway=game_model_gateway,
    )

    reactor_sabotage_use_case = providers.Singleton(
        ReactorSabotageUseCase,
        game_model_gateway=game_model_gateway,
    )

    press_reactor_button_use_case = providers.Singleton(
        PressReactorButtonUseCase,
        game_model_gateway=game_model_gateway,
    )

    can_sabotage_button_use_case = providers.Singleton(
        CanSabotageUseCase,
        game_model_gateway=game_model_gateway,
    )

    electrical_sabotage_use_case = providers.Singleton(
        ElectricalSabotageUseCase,
        game_model_gateway=game_model_gateway,
    )

    flip_switch_use_case = providers.Singleton(
        FlipSwitchUseCase,
        game_model_gateway=game_model_gateway,
    )

    o2_sabotage_use_case = providers.Singleton(
        O2SabotageUseCase,
        game_model_gateway=game_model_gateway,
    )

    enter_code_use_case = providers.Singleton(
        EnterCodeUseCase,
        game_model_gateway=game_model_gateway,
    )

    com_sabotage_use_case = providers.Singleton(
        ComSabotageUseCase,
        game_model_gateway=game_model_gateway,
    )

    rotate_knob_use_case = providers.Singleton(
        RotateKnobUseCase,
        game_model_gateway=game_model_gateway,
    )
