"""宠物管理系统 - 管理真实宠物的信息"""

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / "data"


class Pet:
    """真实宠物信息"""

    def __init__(self, name: str, species: str, breed: str = "",
                 age: float = 0, weight: float = 0, gender: str = "未知"):
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.weight = weight
        self.gender = gender
        self.vaccinations: list[dict] = []
        self.medical_records: list[dict] = []
        self.feeding_schedule: list[dict] = []
        self.notes: list[str] = []
        self.photo_paths: list[str] = []
        self.created_at = datetime.now().isoformat()

    def add_vaccination(self, name: str, date: str, next_date: str = "") -> str:
        record = {"name": name, "date": date, "next_date": next_date}
        self.vaccinations.append(record)
        return f"已记录疫苗: {name} (接种日期: {date})"

    def add_medical_record(self, description: str, date: str,
                           doctor: str = "", cost: float = 0) -> str:
        record = {
            "description": description,
            "date": date,
            "doctor": doctor,
            "cost": cost,
        }
        self.medical_records.append(record)
        return f"已记录医疗信息: {description} (日期: {date})"

    def add_feeding_schedule(self, time: str, food: str, amount: str) -> str:
        schedule = {"time": time, "food": food, "amount": amount}
        self.feeding_schedule.append(schedule)
        return f"已添加喂食计划: {time} - {food} ({amount})"

    def add_note(self, note: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.notes.append(f"[{timestamp}] {note}")
        return f"已添加备注: {note}"

    def profile(self) -> str:
        species_emoji = {
            "猫": "🐱", "狗": "🐶", "兔子": "🐰", "鸟": "🐦",
            "鱼": "🐟", "仓鼠": "🐹", "乌龟": "🐢", "蛇": "🐍",
        }
        emoji = species_emoji.get(self.species, "🐾")

        profile = f"\n{'='*40}\n"
        profile += f"  {emoji} {self.name} 的档案\n"
        profile += f"{'─'*40}\n"
        profile += f"  种类: {self.species}\n"
        if self.breed:
            profile += f"  品种: {self.breed}\n"
        profile += f"  年龄: {self.age} 岁\n"
        profile += f"  体重: {self.weight} kg\n"
        profile += f"  性别: {self.gender}\n"

        if self.vaccinations:
            profile += f"\n  💉 疫苗记录 ({len(self.vaccinations)}):\n"
            for v in self.vaccinations:
                profile += f"    - {v['name']} ({v['date']})"
                if v.get("next_date"):
                    profile += f" | 下次: {v['next_date']}"
                profile += "\n"

        if self.medical_records:
            profile += f"\n  🏥 医疗记录 ({len(self.medical_records)}):\n"
            for r in self.medical_records:
                profile += f"    - {r['description']} ({r['date']})"
                if r.get("doctor"):
                    profile += f" | 医生: {r['doctor']}"
                if r.get("cost"):
                    profile += f" | 费用: ¥{r['cost']}"
                profile += "\n"

        if self.feeding_schedule:
            profile += f"\n  🍽️ 喂食计划:\n"
            for s in self.feeding_schedule:
                profile += f"    - {s['time']}: {s['food']} ({s['amount']})\n"

        if self.notes:
            profile += f"\n  📝 备注 ({len(self.notes)}):\n"
            for n in self.notes[-5:]:  # show last 5
                profile += f"    {n}\n"

        profile += f"{'='*40}\n"
        return profile

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "weight": self.weight,
            "gender": self.gender,
            "vaccinations": self.vaccinations,
            "medical_records": self.medical_records,
            "feeding_schedule": self.feeding_schedule,
            "notes": self.notes,
            "photo_paths": self.photo_paths,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        pet = cls(
            name=data["name"],
            species=data["species"],
            breed=data.get("breed", ""),
            age=data.get("age", 0),
            weight=data.get("weight", 0),
            gender=data.get("gender", "未知"),
        )
        pet.vaccinations = data.get("vaccinations", [])
        pet.medical_records = data.get("medical_records", [])
        pet.feeding_schedule = data.get("feeding_schedule", [])
        pet.notes = data.get("notes", [])
        pet.photo_paths = data.get("photo_paths", [])
        pet.created_at = data.get("created_at", datetime.now().isoformat())
        return pet


class PetManager:
    """宠物管理器"""

    def __init__(self):
        self.pets: dict[str, Pet] = {}
        self.data_file = DATA_DIR / "real_pets.json"
        self._load()

    def _load(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if self.data_file.exists():
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for name, pet_data in data.items():
                self.pets[name] = Pet.from_dict(pet_data)

    def save(self) -> str:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = {name: pet.to_dict() for name, pet in self.pets.items()}
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"已保存 {len(self.pets)} 只宠物的数据"

    def add_pet(self, name: str, species: str, breed: str = "",
                age: float = 0, weight: float = 0, gender: str = "未知") -> str:
        if name in self.pets:
            return f"已存在名为 {name} 的宠物"
        self.pets[name] = Pet(name, species, breed, age, weight, gender)
        self.save()
        return f"🐾 已添加宠物: {name} ({species})"

    def remove_pet(self, name: str) -> str:
        if name not in self.pets:
            return f"找不到名为 {name} 的宠物"
        del self.pets[name]
        self.save()
        return f"已删除宠物: {name}"

    def get_pet(self, name: str) -> Pet | None:
        return self.pets.get(name)

    def list_pets(self) -> str:
        if not self.pets:
            return "还没有添加任何宠物，使用 '添加宠物' 来添加你的第一只宠物！"
        species_emoji = {
            "猫": "🐱", "狗": "🐶", "兔子": "🐰", "鸟": "🐦",
            "鱼": "🐟", "仓鼠": "🐹", "乌龟": "🐢", "蛇": "🐍",
        }
        result = "\n🐾 我的宠物列表:\n"
        result += "─" * 40 + "\n"
        for name, pet in self.pets.items():
            emoji = species_emoji.get(pet.species, "🐾")
            result += f"  {emoji} {name} | {pet.species}"
            if pet.breed:
                result += f" ({pet.breed})"
            result += f" | {pet.age}岁 | {pet.weight}kg\n"
        result += "─" * 40 + "\n"
        result += f"共 {len(self.pets)} 只宠物\n"
        return result

    def upcoming_vaccinations(self) -> str:
        result = "\n💉 即将到来的疫苗提醒:\n"
        result += "─" * 40 + "\n"
        found = False
        for name, pet in self.pets.items():
            for v in pet.vaccinations:
                if v.get("next_date"):
                    result += f"  {name}: {v['name']} - {v['next_date']}\n"
                    found = True
        if not found:
            result += "  暂无疫苗提醒\n"
        result += "─" * 40 + "\n"
        return result
