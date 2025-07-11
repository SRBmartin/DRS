export enum RouteNames {
    LandingRoute  = '',
    LoginRoute = 'login',
    RegisterRoute = 'register',
    DashboardRoute = 'dashboard',
    ProfileRoute = 'profile',
    SurveyRoute = 'survey',
    CreateSurveyRoute = 'create',
    SurveyDetailsRoute = 'details/:survey_id',
    GeneralInformationRoute = 'general-information',
    ChangePasswordRoute = 'change-password',
    DeleteMyAccountRoute = 'delete-my-account',
    AnswerSurveyRoute = 'answer',
    AnswerSurveyEmailRoute = 'mail/:email_id/:survey_id/:response_id/:option',
    AnswerSurveyWebsiteRoute = 'website/:survey_id'
    
};