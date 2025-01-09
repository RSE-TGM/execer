

# execer
## Operational management of Renewable Energy Community (CER Comunità Energetica Rinnovabile)
This code provides operational management for a Renewable Energy Community (CER - Comunità Energetica Rinnovabile) composed by multiple prosumers with PV (PhotoVoltaic) generation systems as well as various energy consumers. Both prosumers and consumers are categorized into five groups—residential, offices, schools, shopping centers, and industrial sites.
To run the code, users supply the PV generation and consumption profiles for each category. These profiles can be adjusted to simulate realistic operating scenarios. For the consumption profiles, it is also possible to define flexibility margins, allowing for demand response strategies within the CER.
The primary goal of the code is to maximize economic returns by increasing collective self-consumption and, when beneficial, selling surplus energy to the grid and potentially deployng into specialized services that enhance the value of exported energy.


##### TOOL INSTRUCTIONS ######



### Excel_Profiles_Data.py
This script imports from an excel file all the profiles used in the optimization.
Either statistical ones for RES, OFF, SCH, COM, IND, and real ones for residentials (provided by SSE department)

The real profiles are sorted in clusters in order to reduce the number of total profiles to optimize, this apporach
reduces computational time requested.
Therefore similar profiles are grouped and treated as a single member of the REC.
The profiles are clustered starting from a correlation matrix (which is saved on the same excel file), where 1 indicates
perfect correspondancy. Then the complementary value is computed as 1 - correlation, this is the distance.
Distance is then used to perform the actual clustering. To define the clusters it is needed to define a maximum distance
under which the whole cluster is taken. The lower is the distance the more are the clusters due to higher precision.



### Parameters.py
This script allows to set ALL parameters needed in the optimization.
    - solver:            IPOPT is the used solver.
                         It can be downloaded from https://www.coin-or.org/download/binary/Ipopt/
                         The used version is Ipopt-3.11.1-win64
                         To implement it the following link "C:\Ipopt-3.11.1-win64-intel13.1\bin" must be added to the
                         System Variables of Windows on PATH section.
                         
                         Linux: install ampl solver: https://coin-or.github.io/Ipopt/INSTALL.html#EXTERNALCODE_ASL
                            git clone https://github.com/coin-or-tools/ThirdParty-ASL.git
                            cd ThirdParty-ASL
                            ./get.ASL
                            ./configure
                            make
                            sudo make install

    - random_set:        flag that enables the random oscillation of the statistical/basic profiles within a certain range

    - flex_range:        flag that enables members/clusters to apply a certain demand side flexibility boundary to the main profiles

    - dynamic_cgrid:     flag that correlates buying grid price to selling grid price, if it is off the buying price is flat and constant

    - period:            defines the number of hours that the optimazer considers in the future (rolling window)

    - starting_hour:     starting point of the simulation

    - duration_hour:     ending point of the simulation

    - REC COMPOSITION:   for each member type cathegory defines the peak power in consumption and production of each single member.
                         to add more members of the same type add more values in the corresponding list. ex: off = [10, 15, 30].
                         note that the number of elements in the same member type lists must be the same
                         ex: off = [10, 15, 30], pv_off = [10, 0, 0] stands for 1 prosumer and 2 consumers.
                         note that the real profiles are already included and therefore not set here.

    - FLEXIBILITY RANGE: flexibility ranges can be set for each type of member and for distinct time intervals.
                         flexibility is considered specular -+X% with respect the the basic profiles.

    - RANDOM RANGE:      random oscillation ranges can be set for each type of member and for distinct time intervals.
                         random oscillation is considered specular -+X% with respect the the basic profiles.
                         it is also applied to the production profiles






