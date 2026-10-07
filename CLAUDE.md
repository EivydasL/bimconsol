# BIM ConSol — repo kontekstas

**Šis repo:** bendri BIM ConSol dalykai (SharePoint site struktūra, brand automatizacija, company-level scriptai).
**NE šis repo:** CRM aplikacijos kodas — tas gyvena atskirai, `github.com/EivydasL/bim-crm`.

**Kanoninis sprendimų žurnalas:** claude.ai Project "BIM ConSol" → `sharepoint-architektura-sprendimas.md`. Jei šis failas ir Project nesutampa, Project laikomas teisingu — atnaujink šį failą pagal jį.

## Kas yra BIM ConSol

- Jungtinis BIM paslaugų brandas: Eivydas Lungys (DeepBIM MB) + Justas Sturis (BIM statyba MB).
- Paslaugos: BIM koordinavimas, mokymai, BIM vadyba, su BIM susijusi duomenų analitika.

## SharePoint

- Tenant: deepbim.sharepoint.com ($0 papildomai, Justas — guest, ne licencijuota paskyra).
- https://deepbim.sharepoint.com/sites/BIMConSol — operacinis site (brand, šablonai, governance).
- https://deepbim.sharepoint.com/sites/BIM_CRM — CRM aplikacija.
- Du atskiri site'ai sąmoningai (permissions riba + brando atskirumas nuo DeepBIM). Galima vėliau sujungti navigaciją per Hub Site, nekeičiant permissions.
- Projektų kodas: prefiksas **BC-0001**.

## Kainos principas ($0 setup)

SharePoint list'os (ne Dataverse) · Power Automate tik standartiniai jungtukai · Power Apps su SharePoint list data source · Power BI Desktop (ne Pro) · Azure App Service F1 free tier.

## Susiję repo

- `bim-crm` (github.com/EivydasL/bim-crm, lokaliai `C:\dev\bim-crm`) — CRM aplikacija, klonuota iš Norberg/"Genranga" šablono. Kodas versijuojamas per git, NE OneDrive (OneDrive gadina `.git` dirbant iš kelių kompiuterių).

## Domenai

- bimconsol.com — aktyvus (Hostinger, iki 2027-10-07).
- bimconsol.lt — registruojamas.
- Pridėjus kaip verified domain prie DeepBIM tenant — galima info@bimconsol.lt be naujo tenant.

## Šio repo struktūra

- `sharepoint/` — provisioning scriptai BIMConSol site bibliotekoms/list'ams (dar nerašyti).
- `brand/` — lokalios brand asset kopijos (logo, brand kit eksportai).
