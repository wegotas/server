2019-05-15

LT:

**Pokyciai serveryje, duomenu bazeje: 4v palaikymo pasalinimas.**
* Duomenu bazes pokyciai:
    * Pasalinti 4v kompiuteriu irasai.
    * bat_to_comp irasai ir rodikles i batteries irasus susijusias tik su 4v kompiuteriais istrinti.
    * ram_to_comp irasai ir rodikles i RAMs irasus susijusius tik su 4v kompiuteriais istrinti.
    * Pasalinti Hdd_sizes, GPUs, Manufacturers irasai kurie neturi rodykliu i juos.
    * Pasalinta lenteles Cpus, hdd_to_comp, Hdd_serials.
    * Is lenteles Computers pasalinti laukai: f_cpu_id, f_gpu_id, f_hdd_size_id, cover, display, bezel, keyboard, mouse, sound, cdrom, hdd_cover, ram_cover.
* Serverio pokyciai:
    * Is modelers:
        * pasalinti modeliai: CPUs, hdd_to_comp, Hdd_serials
        * is Computers pasalinti atributai: f_cpu_id, f_gpu_id, f_hdd_size_id, cover, display, bezel, keyboard, mouse, sound, cdrom, hdd_cover, ram_cover.
    * Is views ir logic pasalinta saukimai 4v kompiuteriu modelius ir ju atributus. Vietoj to perrasytas kodas kad atliktu tuos pacius funkcionalumus be ju.
    * Istrinti nenaudojami failai.
    * Perrasyta dalis kodo norint supaprastinti, pagreitinti veikima ir sumazinti laikinosios atminties naudojima

EN:

**Changes in server, database: 4v support removal.**
* Database changes:
    * Removed 4v computer records.
    * bat_to_comp records and references to batteries records related with deleted 4v computers.
    * ram_to_comp records and references to RAMs records related with deleted 4v computers.
    * Removed Hdd_sizes, GPUs, Manufacturers records which are not referenced by any other record.
    * Removed tables Cpus, hdd_to_comp, Hdd_serials.
    * From table Computers removed fields: f_cpu_id, f_gpu_id, f_hdd_size_id, cover, display, bezel, keyboard, mouse, sound, cdrom, hdd_cover, ram_cover.
* Server changes:
    * From modelers:
        * removed models: CPUs, hdd_to_comp, Hdd_serials.
        * From Computers removed attributes: f_cpu_id, f_gpu_id, f_hdd_size_id, cover, display, bezel, keyboard, mouse, sound, cdrom, hdd_cover, ram_cover.
    * From views and logic removed call to 4v computer models and their attributes. Instead rewritten code to do the same functionality without them.
    * Removed unused files.
    * Rewrittent part of the code in order to simplify it, improve speed and lower ram usage.

___
2019-05-07

LT:

**Pokytis serveryje: Tuscio ramo kaulo pridejimas.**
* Galima prideti tuscia ramo kaula. Jis tures sias savybes:
    * Serial - "Nonexistant"
    * Capacity - "0"
    * Clock - "0"
    * Type - "N/A"
* "Type" yra vienintelis atributas kuri galima keisti. Pagal poreiki kad galima butu pakeisti i DDR2, DDR3, DDR4.

EN:

**Changes in server: Empty ramstick adding.**
* It is possible to add empty rasmtick. It is going to have these attributes:
    * Serial - "Nonexistant"
    * Capacity - "0"
    * Clock - "0"
    * Type - "N/A"
* "Type" is the only attribute which is allowed to be edited. Depending on the need it can be changed to DDR2, DDR3, DDR4.

___
2019-05-03

LT:

**Pokytis serveryje: Ramu kaulu salinimas.**
* Ramu kaulus dabar galima pasalinti paspaudus "x" mygtuka. Jei sis kaulas susietas tik su vienu komputeriu kaulas yra netik atskiriamas nuo kompiuterio, bet ir pats pasalinamas.

EN:
**Changes in server: Ramstick removal.**
* Ramsticks now can be removed by pressing "x" button. If this stick is referenced only by one computer, then not only reference is removed but also stick is removed as well.

___
2019-04-29

LT:

**Pokyciai serveryje: Globalioje paieskoje filtravimas pagal statusa.**
* Dabar galima filtruoti globalios paieskos rezultatus pagal statusa.

EN:

**Changes in server: Global search filtering by status.**
* Now it is possible to filter global search results according to status.

___
2019-04-26

LT:

**Pokyciai serveryje: Paieskos ispletimas.**

* Isplestas lauku kiekis pagal kuriuos atliekama paieska:

    * Seni(palikti):
        * Kompiuterio serialas ('computer_serial')
        * Kita ('other')
        * Gamintojas ('f_manufacturer__manufacturer_name')
        * Isstrizaine ('f_diagonal__diagonal_text')
        * Laikinosios atminties bendra talpa ('f_ram_size__ram_size_text')
        * Vaizdo plokstes pavadinimas 4v ('f_gpu__gpu_name')
        * Modelio pavadinimas ('f_model__model_name')
        * Procesoriaus pavadinimas 4v ('f_cpu__cpu_name')
        * Kliento pavadinimas ('f_sale__f_id_client__client_name')
        * Pardavimo data ('f_sale__date_of_sale')
        * Kaina ('price')
        
	* Nauji(prideti):
        * Vaizdo plokstes pavadinimas 5v ('computergpus__f_id_gpu__gpu_name')
        * Vaizdo plokstes gamintojas 5v ('computergpus__f_id_gpu__f_id_manufacturer__manufacturer_name')
        * Procesoriaus gamintojas 5v ('computerprocessors__f_id_processor__f_manufacturer__manufacturer_name')
        * Procesoriaus modelis 5v ('computerprocessors__f_id_processor__model_name')
        * Procesoriaus standartinis daznis 5v ('computerprocessors__f_id_processor__stock_clock')
        * Procesoriaus auksciausias daznis 5v ('computerprocessors__f_id_processor__max_clock')
        * Procesoriaus fiziniu branduoliu kiekis 5v ('computerprocessors__f_id_processor__cores')
        * Procesoriaus loginiu branduoliu kiekis 5v ('computerprocessors__f_id_processor__threads')
        * Kompiuterio dydzio faktorius ('f_id_computer_form_factor__form_factor_name')
        * Gauta partija ('f_id_received_batches__received_batch_name')
        * Draivo dydzio pavadinimas ('computerdrives__f_drive__f_hdd_sizes__hdd_sizes_name')
        * Draivo greicio pavadinimas ('computerdrives__f_drive__f_speed__speed_name')
        * Draivo sveikata ('computerdrives__f_drive__health')
        * Ekrano kabelio tipas ('f_id_matrix__f_id_cable_type__cable_type_name')
        * Testuotojo pavadinimas ('f_tester__tester_name')
        * Rezoliucijos pavadinimas ('f_id_computer_resolutions__f_id_resolution__resolution_text')
        * Rezoliucijos kategorijos pavadinimas ('f_id_computer_resolutions__f_id_resolution_category__resolution_category_name')
        * Pastabos trumpasis kodas ('computerobservations__f_id_observation__shortcode')
        * Pastabos kategorija ('computerobservations__f_id_observation__f_id_observation_category__category_name')
        * Pastabos subkategorija ('computerobservations__f_id_observation__f_id_observation_subcategory__subcategory_name')
	
	* Atsisakyti:
	    * 'computerobservations__f_id_observation__full_name' - atsisakyta atlikti paieska pagal si lauka nes paieska pagal ji prailgsta is 5s iki 3min. 40s. Tai yra netoleruojama paieskos trukme.

EN:

**Changes in server: Searches extended.**
* Extended fields by which search is executed by:

    * Old(kept):
        * Computer's serial ('computer_serial')
        * Other ('other')
        * Manufacturer ('f_manufacturer__manufacturer_name')
        * Diagonal ('f_diagonal__diagonal_text')
        * Total RAM ('f_ram_size__ram_size_text')
        * GPU name 4v ('f_gpu__gpu_name')
        * Model name ('f_model__model_name')
        * CPU name 4v ('f_cpu__cpu_name')
        * Client's name ('f_sale__f_id_client__client_name')
        * Date of sale ('f_sale__date_of_sale')
        * Price ('price')
        
	* New(added):
        * GPU name 5v ('computergpus__f_id_gpu__gpu_name')
        * GPU name manufacturer 5v ('computergpus__f_id_gpu__f_id_manufacturer__manufacturer_name')
        * Processor's manufacturer 5v ('computerprocessors__f_id_processor__f_manufacturer__manufacturer_name')
        * Processor's model 5v ('computerprocessors__f_id_processor__model_name')
        * Processor's stock clock 5v ('computerprocessors__f_id_processor__stock_clock')
        * Processor's max clock 5v ('computerprocessors__f_id_processor__max_clock')
        * Processor's physical core count 5v ('computerprocessors__f_id_processor__cores')
        * Processor's logical core count 5v ('computerprocessors__f_id_processor__threads')
        * Computer's form factor ('f_id_computer_form_factor__form_factor_name')
        * Received batch ('f_id_received_batches__received_batch_name')
        * Drive's size name ('computerdrives__f_drive__f_hdd_sizes__hdd_sizes_name')
        * Drive's speed name ('computerdrives__f_drive__f_speed__speed_name')
        * Drive's health ('computerdrives__f_drive__health')
        * Screen cable type ('f_id_matrix__f_id_cable_type__cable_type_name')
        * Tester's name ('f_tester__tester_name')
        * Resolution name ('f_id_computer_resolutions__f_id_resolution__resolution_text')
        * Resolution category name ('f_id_computer_resolutions__f_id_resolution_category__resolution_category_name')
        * Observation short code ('computerobservations__f_id_observation__shortcode')
        * Observation category ('computerobservations__f_id_observation__f_id_observation_category__category_name')
        * Observation subcategory ('computerobservations__f_id_observation__f_id_observation_subcategory__subcategory_name')
	
	* Declined:
	    * 'computerobservations__f_id_observation__full_name' - was rejected as a field to search by because search is prolonged from 5s to 3min. 40s. This is intolerable length for search.

___
2019-04-16

LT:

**Pokyciai serveryje: Filtru pasirinkimai rodo draivu kieki su tuo pasirinkimu.**

* Draivai rodo filtru pasirinkimuose to pasirinkimo kieki tarp draivu skliausteliuose (Serial, Model, Size, Lock state, Speed, Form factor, Health, Days on).
    * Si savybe pritaikyta tiek visiem draivam, tiek hdd_order, tiek lot_content lentelese.
* Visu draivu rodomoje lenteleje dabar mygtukai eina ne is virsaus zemyn, bet is kaires desinen isdestymo. Tai netaip isdarko perziuros lentele.
* Pagrindiniame puslapyje aptvarkytos css klases ir kiek kitos klases priskirtos daliai html elementu. Rezultatas: pagrindine lentele nebenukrenta zemyn.

EN:

**Changes in server: Filter choices show drive quantity next to selection.**

* Drives show filter choices show occurance quantity in parenthesis (Serial, Model, Size, Lock state, Speed, Form factor, Health, Days on).
    * This property is applied to all drive viewing, hdd_order and lot_content tables.
* All drive viewing table now has buttons position next to each other horizontally, rather than vertically. It does not distort table that much.
* Main page has css classes tweaked and some classes were assigned to certain html elements. Result: main table no longer drops down.

___
2019-04-15

LT:

**Pokyciai serveryje: Filtrai dabar rodo kompiuteriu kieki savo specifiniuose filtru pasirinkimuose, ten kur tai yra prasminga.**

* Kompiuteriu filtravimo pasirinkimuose skliausteliuose rodo to pasirinkimo pasikartojimo kieki (Manufacturer, Model, CPU, RAM, GPU, Screen, FF/form factor, Tester, Other/Observations).
    * Del cpu ir gpu si kieki rodo tik v5 kompu, del galimu duplikatiniu iskaiciavimo i bendra kieki isvengimo. Todel dalis siu skaiciu gali buti 0 kiekis jei jie yra 4versijos.
* Nuspresta to netaikyti uzsakymuose nes visos ju savybes unikalios.

EN:

**Changes in server: Filters now show quantity of computer in specific filter choices.**

* Computers filtering choices in parenthesis show occurrence quantity (Manufacturer, Model, CPU, RAM, GPU, Screen, FF/form factor, Tester, Other/Observations).
    * Regarding cpu and gpu this quantity is shown only of v5 computers, for avoidance of summing duplicate records into end quantity. Because of that some of these quantities can be shown as 0 if they are of 4th version.
* It was decided to not apply these changes to the orders, because those attributes there are unique.

___
2019-04-10

LT:

**Pokyciai serveryje: daug su daug rysio filtravimo palaikymo ispletimas.**

* CPU ir GPU tinklalapio filtru pasirinkimuose pateikiami tiek daug su vieno, tiek daug su daug sarysiai. Sie pasirinkimai leidzia tvarkingai filtruoti pagal savo esybes.
* Pakeista kaip Others filtruojama: 
    * Komentaro nefiltruoja, del nauju eiluciu problemu.
    * Vietoj komentaro, filtruose pateikiami pastabu pilni pavadinimu pasirinkimai. Sie pasirinkimai leidzia filtruoti pagal pastabu pavadinimus.

EN:

**Changes in server: many to many connection filtering functionality expansion.**

* CPU and GPU website filter choices are provided using both many-to-one and many-to-many connections. These choices allow filtering according to their entities.
* Changes how filtering others work:
    * Comment is no longer being filtered due to newline issues.
    * Instead of comment, filter choices now contain observation names. These coices allow filtering according to observation names.

---
2019-04-09

LT:

**Pokyciai serveryje: Pridetas draivo pasalinimas is computer_editv5**

* Salinimas vyksta paspaudus 'x' mygtuka virs draivo. Jei pasalina sekmingai, draivo html lentele pasalinama is puslapio, priesingu atveju meta alert lentele su html klaidos kodu.

EN:

**Changes in server: Added drive removal from computer_editv5**

* Removal initiates pressing 'x' button above drive. If removal is succesful, drives html table will be removed from page, otherwise alert table will be thrown with html error code.

---
2019-04-09

LT:

**Tinklalapyje sutaisyta problema kai issidarko dizainas pastabu detaliu puslapyje**

EN:

**Fixed and issue when design gets distorted in observation details page**


---
2019-04-04

LT:

**Prideti triju tipu mygtukai, kurie pades lengviau naviguoti kaip draivas susijes su kitais grupem/kompiuteriais**

* 'Lot' mygtukas savije turi partijos pavadinima o ant jo paspaudus naujame lange issoks narsykles langas apie partija.
* 'Order' mygtukas savije turi uzsakymo pavadinima o ant jo paspaudus naujame lange issoks narsykles langas apie uzsakyma.
* 'Open computer' mygtuka paspaudus naujame lange issoks narsykles langas apie kompiuteri. Siu mygtuku gali buti keleta nes tas pats draivas gali buti naudojamas testuojant kelius kompiuterius.

EN:

**Added three types of buttons, which going to help navigating how drive is related to other groups/computers**

* 'Lot' button has lot's name in itself and clicking on it will result in new browser window about lot.
* 'Order' button has order's name in itself and clicking on it will result in new browser window about order.
* 'Open computer' clicking on button will result in new browser window about computer. These button can be several because drive could been used while testing several computers.

---
2019-04-04

LT:

**Kategorijos rodymas kompiuterio paieskos lenteleje is uzsakymu**
* Dabar rodo kategorijas paieskos rezultatu lentelej.
* Prie to paties pastebeta ir istaisyta klaida kai paieskos grazina parduotus ar kitiem uzsakymam priklausancius kompiuterius.

EN:

**Showing categories in computer searching from orders**
* Now category is visible in search result table.
* In addition to that found and fixed a issue when search returns sold and belonging to other orders computers.

---
2019-04-04

LT:

**Pokyciai CSV/Excel eksportavime.**
* Dabar CSV/Excel turi du eksportavimus:
    * Eksportuoti nesiojamus kompiuterius su struktura: "S/N", 'Manufacturer', 'Model', 'CPU', 'RAM', 'GPU', 'HDD', 'Batteries', 'LCD', 'Optical', 'COA', 'Cam', 'Comment', 'Price', 'Box no.'
    * Eksportuoti stacionarius kompiuterius su struktura: "S/N", "Form factor", 'Manufacturer', 'Model', 'CPU', 'RAM', 'GPU', 'HDD', 'Optical', 'COA', 'Comment', 'Price', 'Box no.'
* Jei bent vienas kompiuteris is rinkinio yra stacionarus, eksportuojami visi kaip stacianarus, priesingu atveju visi eksportuojami kaip nesiojami.

EN:

**Changes to CSV/Excel exporting.**
* Now CSV/Excel have two exportations:
    * Exporting laptop computers with structure: "S/N", 'Manufacturer', 'Model', 'CPU', 'RAM', 'GPU', 'HDD', 'Batteries', 'LCD', 'Optical', 'COA', 'Cam', 'Comment', 'Price', 'Box no.'
    * Exporting desktop computers with structure: "S/N", "Form factor", 'Manufacturer', 'Model', 'CPU', 'RAM', 'GPU', 'HDD', 'Optical', 'COA', 'Comment', 'Price', 'Box no.'
* If at least one computer from collection is desktop, then  all are exported as desktop, otherwise all are exported as laptops.

---
2019-04-03

LT:

**Pokyciai serveryje ir duombazes strukturoje: Pridetas formos faktoriaus funkcionalumas.**

* Duombaze laiko formos faktoriaus reiksme.
* Form faktoriai sukuriami tinklalapyje kairiajame meniu.
* Form faktorio reiksme galima priskirti naujam kompiuteriui per klientine programa (konstantino darbas) ir per tinklalapi pridedant nauja irasa. 
* Form faktorio leidziama pakeisti per kompiuterio redagavimo langa tinklalapyje(v4, v5).
* Form faktorius turi savo stulpeli pagrindinioje kompiuteriu rodomoje leneleje. Sioje lenteje galima filtruoti sia reiksme.

**Trumpa versija:**

Igyvendintas form faktoriu funkcionalumas.

EN:

**Changes in server and database structure:**

* Database holds form factor's value.
* Form factors are created in the website's left menu.
* Form factor value can be assigned for a new computer in client program (konstantin's work) and in website when adding a new record.
* Form factor can be changed through computer editing window in a website(v4, v5), 
* Form factor has it's own column in main viewing table of computers. Filters can be applied to it.

**Short version:**

Implemented form factor functionality.

---
2019-03-28

LT:

**Pokyciai serveryje: Pakeistas rankinis kompiuterio iraso pridejimas, kad pridejinetu 5v kompiuterio irasus vietoj 4v.**
* Butini laukai:
    
    "pp" - reiskia yra papildomi pasirinkimai, sarasas kuris issiskleidzia paspaudus kairi peles mygtuka ant iskleidziamo lauko, arba dukart paspaudus ant tekstinio laukelio, rasant i tekstini laukeli yra siulomi papildomi pasirinkimai panasus i vedama. Sio funkcionalumo veikimas smarkiai priklauso nuo naudojamos narsykles ir jos versijos.
     
    * Serial: Kompiuterio seriala galima rasti ant kompiuterio lidpuko, BIOS'e, diagnostines sistemas ar ant motinines plokstes.
    
    * Type(pp): Kompiuterio tipas iprastai yra "Desktop" jei stacionarus arba "Laptop" jei nesiojamas. Ateityje tai gali keistis(tartis su darbu vadovu).
    
    * Category(pp): Kategorija, kuriai sis kompiuteris yra priskirtas(tartis su darbu vadovu).
    
    * Box number(pp): Deze/pozicija ir kuria sis kompiuteris bus padetas sandeliuoti(tartis su darbu vadovu).
    
    * Manufacturer(pp): Kompiuterio gamintoja galima atpazinti pagal logotipa.
    
    * Model(pp): Kompiuterio modeli galima rasti parasyta ant kompiuterio, lipduku, BIOS ar diagnostines sistemas.
    
    * Tester(pp): Testuotojas kuris si kompiuteri suvedineja.
    
    * License(pp): Kompiuterio licenzija galima atpazinti pagal ant jo uzklijuota lipduka. Jei lipduko nera nustatyti "N/A"
    
    * Received batch(pp): Partija su kuria kompiuteris atkeliavo.
    
    * Diagonal(pp): Isstrizaine galima ivertini is akies arba su matavimo priemone. Stacionariems kompiuteriams rasyti "0".
    
    * Observation: Pastaba apie kompiuteri. Butina bent viena pastaba(sis ribotumas skirtas kad atskirti 5v nuo 4v kompus).

* Nebutini laukai:

    * Other: Komentaras apie kompiuteri.
    
    * Total RAM(pp): Viso laikinosios atminties galima atrasti (nevisada) per bios ar diagnostines sistemas.

* Daug su daug esybes ir ju jungtis (Laikinosios atminties kaulas, Procesoriai, Vaizdo plokstes, Pastabos):

    "n" - nauja esybe. Sukuriama nauja tuscia lentele pagal esybes laukus. Dauguma siu lauku tures papildomus pasirinkimus.
    
    "e" - esama esybe. Esybe ieskoma pagal raktazodi is rodomu lauku. Radus tinkamus variantus virs tekstinio lauko bus pateikiami pasiulymai. Paspaudus '+' mygtuka sis variantas bus pridetas kaip lentele prie norimu esybiu rinkinio. Laukai neredaguojami.
    
    * RAM sticks(n, e): Laikinosios atminties kaulus galima issiaiskint praardzius kompiuteri, per bios ar diagnostines sistemas.  
    
    * Processors(n, e): Procesoriu informacija galima issiaiskinti per bios ar diagnostines sistemas. 
        * Procesoriai yra daug-su-daug esybe, nes nors dauguma kompiuteriu turi viena procesoriu, ateityje gali tekti suvedineti serverinius kompiuterius su daugiau nei vienu procesoriumi.
    
    * GPUs(n, e): Vaizdo plokste galima issiaiskinti per bios ar diagnostines sistemas. 
    
    * Observations(e): Pastabos i kurias vertetu atsizvelgti ateityje surinkejams.
    
EN:

**Changes in server: Changed manual computer record adding, so that computer would be added as 5v insteand of 4v.**
* Necessary fields:
    
    "pp" - aditional choices are available, list of possible values appear after left mouse click on listbox, or twice on textbox, writint in textbox also offers similar choices to the one which is being entered. This functionality is highly dependable on web browser used and it's version.
     
    * Serial: Computer serial can be found on a computer's sticker, BIOS, diagnostic system or on motherboard.
    
    * Type(pp): Computer types usually is "Desktop" if it is stationary of "Laptop" if it is laptop. In the future this can change(consult supervisor).
    
    * Category(pp): Category, to which this computer belongs to(consult supervisor).
    
    * Box number(pp): Box/position where computer will be stored(consult supervisor).
    
    * Manufacturer(pp): Computer manufactured can be identified by logo.
    
    * Model(pp): Computer model can be found written on computer, sticker, BIOS or diagnostic system.
    
    * Tester(pp): Tester who is filling in this computer.
    
    * License(pp): Computer license can be identified by sticker. If it is missing set "N/A".
    
    * Received batch(pp): Batch with which computer was received.
    
    * Diagonal(pp): Diagonal can be identified just by looking or measuring tool. Stationary computers write in value "0".
    
    * Observation: Observation about computer. Atleast one observation should be filled in(this requirement exists to be able identify 5v from 4v computer).

* Optional fields:

    * Other: Comment about computer.
    
    * Total RAM(pp): Total random access memory can be found(not always) in BIOS or diagnostic system.

* Many to many entities and their connections (RAMs, Processors, GPUs, observations):

    "n" - new entity. Creates new empty table based on the entity. Most of these fields will have additional choices.
    
    "e" - existing entity. Entity which is found based on the keyword by searchfields. Options which fit the criteria will be displayed above textfield. Pressing "+" button will allow for that option to be added as table in a list wamted entities. Fields are not editable.
    
    * RAM sticks(n, e): Ram sticks can be found by disassembling computer, in BIOS or diagnostic system.
    
    * Processors(n, e): Processor information can be found in BIOS or diagnostic system. 
        * Processors are part of many-to-many entitity because even though most computers have only one processor, in the future records could be added with more than one processor.
    
    * GPUs(n, e): GPU can be found in BIOS or diagnostic system. 
    
    * Observations(e): Observations of which assemblers should be aware of.

---
2019-03-14

LT:

**Pokyciai serveryje: Pridetas funkcionalumas redaguoti daug su daug rysius 5versijos kompiuteriuose.**
* Laikinos atminties leidzia keisti tik tipa. Seriala, dydi ir dazni neleis nes juos turi imti per klientine programa.
    Issaugojama paspaudus issaugojimo mygtuka.
* Procesoriuose Gamintoja, Modeli, standartini dazni, maksimalu dazni, fizini ir logini branduoliu kieki leidzia redaguoti.
    Redaguojamas procesorius keicia procesoriaus irasa tik viename kompiuteryje o ne visuose kuriuose sis procesorius pasikartoja.
    Fizinis ir loginis branduoliu kiekis yra leidziamas ivesti tik sveikas skaicius.
    Issaugojama paspaudus issaugojimo mygtuka.
* Vaizdo plokste Gamintoja ir vaizdo plokstes pavadinima leidzia redaguoti.
    Redaguojama vaizdo plokste keicia vaizdo plokstes irasa tik viename kompiuteryje o ne visuose kuriuose si vaizdo plokste pasikartoja.
    Issaugojama paspaudus issaugojimo mygtuka.
* Draivu(HDD/SSD) redaguoti per computer_edit_v5 puslapi neleis. Vietoj to yra mygtukas "Edit drive" kuris atidaro draivo redagavimo puslapi, kuriame leis redaguoti pati draiva.
    Vienas draivas iprastai yra suristas su vienu kompiuteriu. Retais atvejais vienas draivas suristas buna su keliais kompiuteriais. Tokiais atvejais pakeitus sio draivo informacija, pasikeis duomenis visuose kompiuteriuiose kuriuose sis draivas yra priskirtas.
    Issaugojama per "Edit_drive" mygtuko atsidariusiame puslapyje.
* Observation'ai ieskomi, pridedami ir salinami paciame puslapyje. Jei pokytis matosi puslapyje, vadinas tas pokytis ir ivyko.
    Observation'ai ieskomi ivedant i tekstini laukeli raktazodzius ir paspaudus "Enter". Virs tekstinio laukelio islenda lentele su observation'u rezultatais. Sie rezultatai yra atrenkami pagal tai kurie dar nepriskirti kompiuteriui ir atitinka raktazodzius perskirtus tarpais. Siose rezultatu lentelese yra mygtukai "+", jie priskiria atitinkama observation'a prie redaguojamo kompiuterio.
    Observation'ai salinami paspaudus "x" mygtuka prie norimo pasalinti observation'o.

**Trumpa versija:**
* Laikina atmintis, Procesoriai ir Vaizdo plokstes atsinaujina paspaudus issaugojimo mygtuka.
* Draivai per "Edit_drive" mygtuka atsidaranciame puslapyje saugojimi.
* Observation'u sarysiai keiciami javascripto uzklausom. Jeigu matosi pokytis puslapyje, vadinas issaugojimas ivyko.




EN

**Changes in server: Added functionality to edit many to many relationships in 5th version computers.**
* RAM allows changing only memory type. Serial, capacity, clock is not allowed to edit, because they should be entered through a client program.
    Saves when pressed saving button.
* Processor Manufacturer, Model, Stock clock, Max clock, Core count and Thread count are allowed to be modified.
    Edited processor is changed only for that computer only, not on all computers where that processor is used on.
    Core count and Thread count are allowed as integers only.
    Saves when pressed saving button.
* GPU Manufacturer and gpu_name are allowed to be modified.
    Edited GPU is changed only for that computer only, not on all computers where that GPU is used on.
    Saves when pressed saving button.
* Drives(HDD/SSD) editing from computer_edit_v5 is not available. Instead there is a button "Edit drive" which opens drive editing, which allows drive editing.
    One drive is usually assigned to a one computer. In rare cases one drive could be assigned to a several computers. In these cases changing drive information, will change data in all computers where that drives is assigned to.
    Saves in "Edit_drive" button's opened page.
* Observations searched, assigned and removed assignation in the same page. If change is visible in page, that means that change has happened.
    Observations are searched by inputing keyword in text box and pressing "Enter". Table with results of observations appears above textbox. These results are selected according to what was unassigned to a present computer and according to a keyword split by spaces. These results in tables have buttons "+", which assigns corresponing observation to a edited computer.
    Observations are removed by pressing "x" button next to observation that needs to be removed.


**Short version:**
* RAMs, Processors and GPUs are edited on pressing save button.
* Drives are saved on page which is opened by pressing "Edit_drive" button.
* Observations relations are changed using javascript calls. If change is visible in the page, that means change has happened.
---