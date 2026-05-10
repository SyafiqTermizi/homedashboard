import enum


class Frequency(enum.StrEnum):
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class Location(enum.StrEnum):
    JHR01 = ("JHR01" , "Pulau Aur dan Pulau Pemanggil ")
    JHR02 = ("JHR02" , "Johor Bahru, Kota Tinggi, Mersing, Kulai")
    JHR03 = ("JHR03" , "Kluang, Pontian")
    JHR04 = ("JHR04" , "Batu Pahat, Muar, Segamat, Gemas Johor, Tangkak")
    KDH01 = ("KDH01" , "Kota Setar, Kubang Pasu, Pokok Sena (Daerah Kecil)")
    KDH02 = ("KDH02" , "Kuala Muda, Yan, Pendang")
    KDH03 = ("KDH03" , "Padang Terap, Sik")
    KDH04 = ("KDH04" , "Baling")
    KDH05 = ("KDH05" , "Bandar Baharu, Kulim")
    KDH06 = ("KDH06" , "Langkawi")
    KDH07 = ("KDH07" , "Puncak Gunung Jerai")
    KTN01 = ("KTN01" , "Bachok, Kota Bharu, Machang, Pasir Mas, Pasir Puteh, Tanah Merah, Tumpat, Kuala Kr")
    KTN02 = ("KTN02" , "Gua Musang (Daerah Galas Dan Bertam), Jeli, Jajahan Kecil Lojing")
    MLK01 = ("MLK01" , "SELURUH NEGERI MELAKA")
    NGS01 = ("NGS01" , "Tampin, Jempol")
    NGS02 = ("NGS02" , "Jelebu, Kuala Pilah, Rembau")
    NGS03 = ("NGS03" , "Port Dickson, Seremban")
    PHG01 = ("PHG01" , "Pulau Tioman")
    PHG02 = ("PHG02" , "Kuantan, Pekan, Muadzam Shah")
    PHG03 = ("PHG03" , "Jerantut, Temerloh, Maran, Bera, Chenor, Jengka")
    PHG04 = ("PHG04" , "Bentong, Lipis, Raub")
    PHG05 = ("PHG05" , "Genting Sempah, Janda Baik, Bukit Tinggi")
    PHG06 = ("PHG06" , "Cameron Highlands, Genting Higlands, Bukit Fraser")
    PHG07 = ("PHG07" , "Zon Khas Daerah Rompin, (Mukim Rompin, Mukim Endau, Mukim Pontian)")
    PLS01 = ("PLS01" , "Kangar, Padang Besar, Arau")
    PNG01 = ("PNG01" , "Seluruh Negeri Pulau Pinang")
    PRK01 = ("PRK01" , "Tapah, Slim River, Tanjung Malim")
    PRK02 = ("PRK02" , "Kuala Kangsar, Sg. Siput , Ipoh, Batu Gajah, Kampar")
    PRK03 = ("PRK03" , "Lenggong, Pengkalan Hulu, Grik")
    PRK04 = ("PRK04" , "Temengor, Belum")
    PRK05 = ("PRK05" , "Kg Gajah, Teluk Intan, Bagan Datuk, Seri Iskandar, Beruas, Parit, Lumut, Sitiaw")
    PRK06 = ("PRK06" , "Selama, Taiping, Bagan Serai, Parit Buntar")
    PRK07 = ("PRK07" , "Bukit Larut")
    SBH01 = ("SBH01" , "Bahagian Sandakan (Timur), Bukit Garam, Semawang, Temanggong, Tambisan, Banda")
    SBH02 = ("SBH02" , "Beluran, Telupid, Pinangah, Terusan, Kuamut, Bahagian Sandakan (Barat)")
    SBH03 = ("SBH03" , "Lahad Datu, Silabukan, Kunak, Sahabat, Semporna, Tungku, Bahagian Tawau (Timur)")
    SBH04 = ("SBH04" , "Bandar Tawau, Balong, Merotai, Kalabakan, Bahagian Tawau (Barat)")
    SBH05 = ("SBH05" , "Kudat, Kota Marudu, Pitas, Pulau Banggi, Bahagian Kudat")
    SBH06 = ("SBH06" , "Gunung Kinabalu")
    SBH07 = ("SBH07" , "Kota Kinabalu, Ranau, Kota Belud, Tuaran, Penampang, Papar, Putatan, Bahagian Panta")
    SBH08 = ("SBH08" , "Pensiangan, Keningau, Tambunan, Nabawan, Bahagian Pendalaman (Atas)")
    SBH09 = ("SBH09" , "Beaufort, Kuala Penyu, Sipitang, Tenom, Long Pasia, Membakut, Weston")
    SGR01 = ("SGR01" , "Gombak, Petaling, Sepang, Hulu Langat, Hulu Selangor, S.Alam")
    SGR02 = ("SGR02" , "Kuala Selangor, Sabak Bernam")
    SGR03 = ("SGR03" , "Klang, Kuala Langat")
    SWK01 = ("SWK01" , "Limbang, Lawas, Sundar, Trusan")
    SWK02 = ("SWK02" , "Miri, Niah, Bekenu, Sibuti, Marudi")
    SWK03 = ("SWK03" , "Pandan, Belaga, Suai, Tatau, Sebauh, Bintulu")
    SWK04 = ("SWK04" , "Sibu, Mukah, Dalat, Song, Igan, Oya, Balingian, Kanowit, Kapit")
    SWK05 = ("SWK05" , "Sarikei, Matu, Julau, Rajang, Daro, Bintangor, Belawai")
    SWK06 = ("SWK06" , "Lubok Antu, Sri Aman, Roban, Debak, Kabong, Lingga, Engkelili, Betong, Spaoh, Pusa")
    SWK07 = ("SWK07" , "Serian, Simunjan, Samarahan, Sebuyau, Meludam")
    SWK08 = ("SWK08" , "Kuching, Bau, Lundu, Sematan")
    SWK09 = ("SWK09" , "Zon Khas (Kampung Patarikan)")
    TRG01 = ("TRG01" , "Kuala Terengganu, Marang, Kuala Nerus")
    TRG02 = ("TRG02" , "Besut, Setiu")
    TRG03 = ("TRG03" , "Hulu Terengganu")
    TRG04 = ("TRG04" , "Dungun, Kemaman")
    WLY01 = ("WLY01" , "Kuala Lumpur, Putrajaya")
    WLY02 = ("WLY02" , "Labuan")

    def __new__(cls, value, description):
        obj = str.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj
