from pydantic import BaseModel, EmailStr


class Education(BaseModel):
    university: str | None  # “Образование до РЭШ 1: университет”
    department: str | None  # “Департамент”
    specialty: str | None  # “Специальность”
    specialization: str | None  # “Специализация”


class PostEducation(BaseModel):
    university: str | None  # “Образование после РЭШ 1: университет”
    location: str | None  # “Местонахождение”
    department: str | None  # “Департамент”
    program_type: str | None  # “Тип программы”
    program: str | None  # “Программа”
    degree: str | None  # “Полученная степень”
    period: str | None  # “Период обучения”
    completed: bool | None  # “Окончено?”


class WorkExperience(BaseModel):
    work_industry: str | None  # “Основное место работы: отрасль”
    work_subindustry: str | None  # “Подотрасль”
    work_company: str | None  # “Компания”
    work_location: str | None  # “Местонахождение”
    work_office: str | None  # “Офис”
    work_department: str | None  # “Департамент”
    work_position: str | None  # “Должность”
    work_tenure: str | None  # “Tenure”


class NesUserInfo(BaseModel):
    nes_id: int  # “my.nes ID”
    name: str  # “ФИО”

    # Personal info
    address: str | None  # “Фактический адрес”
    city: str | None  # “Город”
    region: str | None  # “Регион”
    country: str | None  # “Страна”

    # NES alumni info
    program: str  # “программа”
    class_name: str | None  # “Класс”
    diploma_received: bool | None  # “Получен диплом РЭШ”

    # Contacts
    email_primary: EmailStr | None  # “E-mail основной”
    email_secondary: EmailStr | None  # “E-mail резервный”
    mobile_phone: str | None  # “Мобильный телефон”
    work_phone: str | None  # “Рабочий телефон”
    homepage_social: str | None  # “Домашняя страница, соцсети”

    # NES specific
    research_interests: list[str]  # “Исследовательские интересы”
    certificates: list[str]  # “Сертификаты”

    # Hobbies and expertision
    hobbies: list[str]  # “Хобби”
    industry_expertise: list[str]  # “Экспертиза по отраслям”
    country_expertise: list[str]  # “Экпертиза по странам”
    professional_expertise: list[str]  # “Профессиональная экспертиза”

    main_work: WorkExperience | None
    additional_work: list[WorkExperience] = []

    pre_nes_education: list[Education] = []
    post_nes_education: list[PostEducation] = []
