from pydantic import BaseModel, EmailStr, Field


class Education(BaseModel):
    university: str | None = Field(default=None, description="Университет")
    department: str | None = Field(default=None, description="Департамент")
    specialty: str | None = Field(default=None, description="Специальность")
    specialization: str | None = Field(default=None, description="Специализация")


class PostEducation(BaseModel):
    university: str | None = Field(default=None, description="Университет")
    location: str | None = Field(default=None, description="Местонахождение")
    department: str | None = Field(default=None, description="Департамент")
    program_type: str | None = Field(default=None, description="Тип программы")
    program: str | None = Field(default=None, description="Программа")
    degree: str | None = Field(default=None, description="Полученная степень")
    period: str | None = Field(default=None, description="Период обучения")
    completed: bool | None = Field(default=None, description="Окончено?")


class WorkExperience(BaseModel):
    work_industry: str | None = Field(default=None, description="Отрасль")
    work_subindustry: str | None = Field(default=None, description="Подотрасль")
    work_company: str | None = Field(default=None, description="Компания")
    work_location: str | None = Field(default=None, description="Местонахождение")
    work_office: str | None = Field(default=None, description="Офис")
    work_department: str | None = Field(default=None, description="Департамент")
    work_position: str | None = Field(default=None, description="Должность")
    work_tenure: str | None = Field(default=None, description="Tenure")


class NesUserInfo(BaseModel):
    nes_id: int = Field(description="my.nes ID")

    # Personal info
    name: str = Field(description="ФИО")
    address: str | None = Field(default=None, description="Фактический адрес")
    city: str | None = Field(default=None, description="Город")
    region: str | None = Field(default=None, description="Регион")
    country: str | None = Field(default=None, description="Страна")

    # NES alumni info
    program: str | None = Field(default=None, description="программа")
    class_name: str | None = Field(default=None, description="Класс")
    diploma_received: bool | None = Field(
        default=None, description="Получен диплом РЭШ"
    )

    # Contacts
    email_primary: EmailStr | None = Field(default=None, description="E-mail основной")
    email_secondary: EmailStr | None = Field(
        default=None, description="E-mail резервный"
    )
    mobile_phone: str | None = Field(default=None, description="Мобильный телефон")
    work_phone: str | None = Field(default=None, description="Рабочий телефон")
    homepage_social: str | None = Field(
        default=None, description="Домашняя страница, соцсети"
    )

    # NES specific
    research_interests: list[str] | None = Field(
        default=None, description="Исследовательские интересы"
    )
    certificates: list[str] | None = Field(default=None, description="Сертификаты")

    # Hobbies and expertise
    hobbies: list[str] | None = Field(default=None, description="Хобби")
    industry_expertise: list[str] | None = Field(
        default=None, description="Экспертиза по отраслям"
    )
    country_expertise: list[str] | None = Field(
        default=None, description="Экпертиза по странам"
    )
    professional_expertise: list[str] | None = Field(
        default=None, description="Профессиональная экспертиза"
    )

    main_work: WorkExperience | None = Field(
        default=None, description="Основное место работы"
    )
    additional_work: list[WorkExperience] | None = Field(
        default=None, description="Дополнительные места работы"
    )

    pre_nes_education: list[Education] | None = Field(
        default=None, description="Образование до РЭШ"
    )
    post_nes_education: list[PostEducation] | None = Field(
        default=None, description="Образование после РЭШ"
    )
