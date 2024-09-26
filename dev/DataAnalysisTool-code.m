
classdef DataAnalysisTool < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        DataAnalysisToolUIFigure        matlab.ui.Figure
        Menu                            matlab.ui.container.Menu
        ExportMenu                      matlab.ui.container.Menu
        PredictionPlotMenu              matlab.ui.container.Menu
        DataofClustersMenu              matlab.ui.container.Menu
        ExcelxlsxMenu                   matlab.ui.container.Menu
        MatlabmatMenu                   matlab.ui.container.Menu
        MeasurementDatabaseMenu         matlab.ui.container.Menu
        ExcelxlsxMenu_2                 matlab.ui.container.Menu
        MatlabmatMenu_2                 matlab.ui.container.Menu
        TranslationTableMenu            matlab.ui.container.Menu
        SettingsMenu                    matlab.ui.container.Menu
        GridLayout                      matlab.ui.container.GridLayout
        ShowComparisonCheckBox          matlab.ui.control.CheckBox
        TabGroup                        matlab.ui.container.TabGroup
        OverviewTab                     matlab.ui.container.Tab
        Axes_Predicted_Envelopes        matlab.ui.control.UIAxes
        freqbasedClustersTab            matlab.ui.container.Tab
        freqClustersAxes                matlab.ui.control.UIAxes
        compbasedClustersTab            matlab.ui.container.Tab
        componentbasedClustersAxes      matlab.ui.control.UIAxes
        positionbasedClustersTab        matlab.ui.container.Tab
        positionbasedClustersAxes       matlab.ui.control.UIAxes
        CoGPositionsTab                 matlab.ui.container.Tab
        CoGPositionsAxes                matlab.ui.control.UIAxes
        LinkageTab                      matlab.ui.container.Tab
        LinkagePlotAxes                 matlab.ui.control.UIAxes
        ClusteringMethodsPanel          matlab.ui.container.Panel
        positionbasedCheckBox           matlab.ui.control.CheckBox
        componentbasedCheckBox          matlab.ui.control.CheckBox
        frequencybasedCheckBox          matlab.ui.control.CheckBox
        ClusterButton                   matlab.ui.control.Button
        PredictionResultsPanel          matlab.ui.container.Panel
        positionbased_Shape             matlab.ui.control.EditField
        positionbased_Mag               matlab.ui.control.EditField
        positionbasedEditFieldLabel     matlab.ui.control.Label
        componentbased_Shape            matlab.ui.control.EditField
        componentbased_Mag              matlab.ui.control.EditField
        componentbasedEditFieldLabel    matlab.ui.control.Label
        ShapeerrorTextAreaLabel         matlab.ui.control.Label
        ShapeerrorTextArea              matlab.ui.control.TextArea
        MagnitudeerrorTextArea          matlab.ui.control.TextArea
        MagnitudeerrorTextAreaLabel     matlab.ui.control.Label
        freqbasedLabel                  matlab.ui.control.Label
        alternativeselectionmethodSwitch  matlab.ui.control.Switch
        alternativeselectionmethodSwitchLabel  matlab.ui.control.Label
        FunctionSelectionButtonGroup    matlab.ui.container.ButtonGroup
        CompareButton                   matlab.ui.control.RadioButton
        PredictButton                   matlab.ui.control.RadioButton
        EditField                       matlab.ui.control.NumericEditField
        EditFieldLabel                  matlab.ui.control.Label
        frequencyrangeHzEditField       matlab.ui.control.NumericEditField
        frequencyrangeHzEditFieldLabel  matlab.ui.control.Label
        CustomNumberofSuperclustersPanel  matlab.ui.container.Panel
        NumberofSuperclustersEditField  matlab.ui.control.EditField
        UpdateFilesforComparisonButton  matlab.ui.control.Button
        ComponentLabel                  matlab.ui.control.Label
        SelectComponentEditField        matlab.ui.control.EditField
        SelectedDirectionsPanel         matlab.ui.container.Panel
        ZCheckBox_2                     matlab.ui.control.CheckBox
        ZCheckBox                       matlab.ui.control.CheckBox
        YCheckBox_2                     matlab.ui.control.CheckBox
        YCheckBox                       matlab.ui.control.CheckBox
        XCheckBox_2                     matlab.ui.control.CheckBox
        XCheckBox                       matlab.ui.control.CheckBox
        SelectedBuilstagesPanel         matlab.ui.container.Panel
        NotfoundCheckBox                matlab.ui.control.CheckBox
        KEXCheckBox                     matlab.ui.control.CheckBox
        FBCheckBox                      matlab.ui.control.CheckBox
        SERIECheckBox                   matlab.ui.control.CheckBox
        VS1CheckBox                     matlab.ui.control.CheckBox
        VS2CheckBox                     matlab.ui.control.CheckBox
        ASCheckBox                      matlab.ui.control.CheckBox
        BS0CheckBox                     matlab.ui.control.CheckBox
        BS1CheckBox                     matlab.ui.control.CheckBox
        DataPreparationButton           matlab.ui.control.Button
        ComparetoyearLabel              matlab.ui.control.Label
        MeasurementFileforComparisonDropDownLabel  matlab.ui.control.Label
        MeasurementFileforComparisonDropDown  matlab.ui.control.DropDown
        SetupButton                     matlab.ui.control.Button
        ReferenceYearDropDown           matlab.ui.control.DropDown
        CompareDataButton               matlab.ui.control.Button
        AltSelectionField               matlab.ui.control.EditField
        MeasurementSelection            matlab.ui.container.CheckBoxTree
        EnvelopeGenerationMethodButtonGroup  matlab.ui.container.ButtonGroup
        PredictionDropDown              matlab.ui.control.DropDown
        PredictionDropDownLabel         matlab.ui.control.Label
        ClusterDropDown                 matlab.ui.control.DropDown
        ClusterDropDownLabel            matlab.ui.control.Label
    end

    properties (Access = private)
        treenodes = cell(1,1)   % Nodes in the selection tree
        readPaths  % List of directories to read from
        CoGfiles   % List of Files with CoG data

        Wheelbase = cell(1,2); % cell array {i,1} = Buildseries, {i,2} = Wheelbase

        %min and max frequency for Lvl2 Custering
        min_freq % min 4 because of txt-data
        max_freq % max 3200 because of txt data
        loIndex % Description
        fSteps % Description
        faultyData % Description
        spectr % Description
        freqres = 4; %frequency resolution in Hz
        spectr_outdated = false;

        Measurement_Database % Description
        NumberOfSuperClusters % Description
        srtdEnvs
        srtdMems % Description
        Selected_ModelSeriesstring
        Selected_Buildstages
        sEnvs_freq % Description
        sMems_freq
        matchidx % Description
        SelectionCell % Description
        error_ind % Description
        SettingsAppHandle  %Handle for Settings App
        euclidian_metrics = ['euclidean','seuclidean']; % list of euclidian distance metrics
        realPrediction = false %determines if a real prediction without comparison data is run
        srtdEnvsC   % sorted Envelopes of component based clustering
        srtdMemsC   % sorted Members of component based clustering
        srtdCompsC  % sorted Components of Component based clustering
        sMemsC      % Supercluster Members of Component based clustering
        sEnvsC      % Superclusters of Component based clustering
        addData = false    % bool var to decide wether to update data perparation for all folders or only new ones

        superEnvMethod = 'Maximum'; % Method to generate super Envelopes e.g. "Maximum", "Mean"
        predictMthd = 'Maximum'; %Method to use for calculation of prediction envelopes

        %Hüllkurven, Member und Componentenliste der ausgewählten Cluster
        %für die drei Clustermethoden
        selectedEnvs_Comp
        selectedEnvs_CoG
        selectedEnvs_freq
        selectedMems_freq
        selectedMems_Comp
        selectedMems_CoG
        selectedComp_Comp
        selectedComp_CoG
        selectedComp_freq

        %Generated prediction Envelopes
        pE_Comparison %of all Comparison Files
        pE_C          %of component based Clustering
        pE_freq       %of freq based Clustering
        pE_CoG        %of CoG based Clustering

        %Übersetzungstabelle für Bauteile aus CoG-Daten
        trans_tab

        %sorted Members, Envelopes and Components of CoG based clustering
        srtdCompsCoG
        srtdEnvsCoG
        srtdMemsCoG
        sEnvsCoG
        sMemsCoG

        % Data for Plotting CoGs
        CoGs_real   %CoGs of each component
        Comps_trans_real    %component
        ClstrIdx_CoG % idx of Cluster
        CoGCluster_valid % bool var which saves if any data for CoG based clustering is available

        file_path % Path of app
    end

    properties (Access = public)
        %properties set to public are accessed by other called apps e.g. settings app

        kMeans_distMetric = 'correlation'; % distance metric for kMeans Clustering
        hierachical_distMetric = 'seuclidean'; % distance metric for hierachical Clustering
        freqClstr_threshold = 0.3; %threshold for selection of automated number of superclusters
        use_hierachical = true;    %bool var which decides if hierachical clustering is used
        use_kMeans = false;        %bool var which decides if kMeans clustering is used
        customClstrNumber = false; %bool var which decides wether to use automated Clustering or not
        NCoGClusters = 6; % Number of Clusters for CoG Clustering
        method_freq = "hierachical"; % Cluster Method for frequency based Clustering
        method_CoG  = "hierachical"; % Cluster Method for position based Clustering
        cluster_woMotor = false; % boolean variable which decides wether to exclude component "Motor" from clustering
    end

    methods (Access = private)
        %reads selected frequency band from GUI and stores them into private app vars
        function updateSelectedFrequencies(app)
            %spectrum of interest, lower and upper in Hz
            app.min_freq = app.frequencyrangeHzEditField.Value;
            app.max_freq = app.EditField.Value;
            if app.max_freq <= app.min_freq
                uialert(app.DataAnalysisToolUIFigure,append("Lower frequency is equal or higher than upper frequency",newline,"Please update frequencies before clustering!")...
                    ,"Error while updating frequency bounds");
            else
                app.spectr = [app.min_freq, app.max_freq];
                app.loIndex = app.spectr(1)/app.freqres;
                app.fSteps = (app.spectr(2)-app.spectr(1))/app.freqres;
            end

            app.spectr_outdated = true;
        end

        %Reads Measurementdata from textfiles
        function [names,data,components,numberOfFiles,falseData] = ReadData(~,files,Database)
            %readData reads in given file path and returns array of data, cell of
            %file names and number of files extracted.

            n = 1;
            k = 1;
            dtb_idx = 1;
            falseData(1) = string(0);
            for i = 1:length(files)
                file        = append(files(i).folder,'\',files(i).name);
                checkData   = load(file);
                if length(checkData) ~= 800 || contains(file,"Kopie")
                    falseData(n) = file;
                    n = n+1;
                    disp(append("found invalid data: ",file))
                    if length(checkData) ~= 800; dtb_idx = dtb_idx +1; end
                    clear checkData
                    continue
                end
                data(:,:,k)             = checkData;
                names(k)                = {string(files(i).name)};
                components(k,1)         = Database(dtb_idx).Bauteil;
                k = k+1;
                dtb_idx = dtb_idx +1;
            end
            numberOfFiles = length(files)-n;
        end

        %creates Database of all found Measurement sand saves the it to app.MeasurementDatabase
        function CreateDatabase(app)
            names_all = cell(length(app.readPaths),3);

            for i = 1:length(app.readPaths)
                names_all{i,2} = app.readPaths(i).folder;
                current_dir = dir(append(app.readPaths(i).folder,'\', app.readPaths(i).name,'\**\K*.txt'));

                names = cell(length(current_dir),1);
                subfolders = cell(length(current_dir),1);
                for j = 1:length(current_dir)
                    names{j}                = string(current_dir(j).name);
                    subfolders_cell         = split(current_dir(j).folder,names_all{i,2});
                    subfolders(j,1)         = subfolders_cell(2,1);
                end
                names_all{i,1} = names;
                names_all{i,3} = subfolders;
            end
            %Zählen der leeren Ordner
            empty_folder_vec = false(length(names_all),1);
            for i = 1: length(names_all)
                if isempty(names_all{i,1})
                    empty_folder_vec(i)=true;
                end
            end
            %Bestimmen der Gesamtanzahl der Versuche und zählen der Dateien mit dem
            %Wort "Kopie" im Namen, um diese von der weiteren Auswertung auszuschließen
            %Gesamtanzahl der gültigen Textdateien wird benötigt, um Speicher für die
            %Datenbank anzufordern.
            Anzahl_versuche = 0;
            kopie_count = 0;
            kopie_idx = zeros(30,2);
            len_vec = zeros(length(names_all),1);
            for i = 1:length(names_all)
                if ~empty_folder_vec(i)
                    Anzahl_versuche = Anzahl_versuche + length(names_all{i,1});
                    len_vec(i) = length(names_all{i,1});
                end
                for j = 1:length(names_all{i,1})
                    if contains(names_all{i,1}{j,1},"Kopie")
                        kopie_count = kopie_count + 1;
                        kopie_idx(kopie_count,1) = i;
                        kopie_idx(kopie_count,2) = j;

                    end
                end
            end

            Anzahl_versuche = Anzahl_versuche - kopie_count;

            %Speicherallokierung für Datenbank
            Versuche(Anzahl_versuche) = struct("ID",zeros(1,1),"Dateiname",strings(1,1),"Pfad",strings(1,1),...
                "Unterpfad",strings(1,1),"Jahr",strings(1,1),"Baureihe",strings(1,1),...
                "Nummer",strings(1,1),"Bauteil",strings(1,1),"Baustufe",strings(1,1),"Richtung",strings(1,1),...
                "Last",strings(1,1),"Gang",strings(1,1));

            %Zur Verwendung von Regular Expressions siehe Matlab Dokumentation zu
            %"Regular Expressions"
            expression = "(?<Baureihe>[KMAR]+\d*)_?(?>\sMUE2|MÜ_Funtionsba_-|-20|_-|_TUE)*_*(?<Nummer>V?\d{6})?_\d\d\.\d\d\.(?<Jahr>\d{4})_(?<Bauteil>.+)_(?<Richtung>[\+-][XYZ])?S?_(?<Last>GL|VL|GS)[_-]HL_(?<Gang>\d)";
            exp_Baustufe = ".*_(?<Baustufe>Kex|KEX|BS\d|FB|VS\d|AS|S|Serie)_.*";
            exp_Nummer = ".*(?<Nummer>\d{6}).*";

            current_pos = 0;
            for i = 1:length(names_all)                 %Schleife die durch alle gefundenen Ordner iteriert

                if ~empty_folder_vec(i)                %Abfangen von leeren Ordnern
                    m = 0;

                    %Auswerten des Ordnerpfads für Infos zu Baustufe und Nummer
                    tmp_Baustufe = regexp(names_all{i,2},exp_Baustufe,"names");
                    tmp_Nummer = regexp(names_all{i,2},exp_Nummer,"names");

                    for j = 1: length(names_all{i,1})   %Schleife, die durch alle Dateien in einem Ordner iteriet
                        if ~contains(names_all{i,1}{j,1},"Kopie")                   %schließt 30 files, bei denen Informationen im Titel fehlen und "Kopie" im Titel steht aus
                            m = m + 1;
                            k = current_pos + m;            %Index in der Datenbank
                            tmp = regexp(names_all{i,1}{j,1},expression,'names','once');   %Auswerten des Dateinamen nach Eigenschaften

                            Versuche(k).Dateiname = names_all{i,1}{j,1};
                            Versuche(k).Pfad = string(names_all{i,2});
                            Versuche(k).Unterpfad = string(names_all{i,3}{j,1});
                            Versuche(k).Jahr = tmp.Jahr;
                            Versuche(k).Baureihe = tmp.Baureihe;

                            if contains(tmp.Nummer,"V")
                                Versuche(k).Nummer = tmp.Nummer;
                            elseif tmp.Nummer ~= "" && ~contains(tmp.Nummer,"V")
                                Versuche(k).Nummer = append("V",tmp.Nummer);
                            elseif string(tmp_Nummer.Nummer) ~= ""
                                Versuche(k).Nummer = append("V",tmp_Nummer.Nummer);
                            end
                            Versuche(k).ID = k;
                            Versuche(k).Bauteil = tmp.Bauteil;
                            Versuche(k).Richtung = tmp.Richtung;
                            Versuche(k).Last = tmp.Last;
                            Versuche(k).Gang = tmp.Gang;
                            Versuche(k).Baustufe = upper(string(tmp_Baustufe.Baustufe));
                        end
                    end

                    %Erhöhung der Position in der Datenbank um die Anzahl der Dateien
                    %aus dem eingelesenen Ordner
                    current_pos = current_pos + m;
                end
            end
            % Ersetzen von leeren Einträgen in der Datenbank
            %um Fehler bei der Konvertierung zu array zu vermeiden.
            for i = 1:length(Versuche)
                if isempty(Versuche(i).Baureihe) || Versuche(i).Baureihe == ""
                    Versuche(i).Baureihe = "Not found";
                end
                if isempty(Versuche(i).Nummer) || Versuche(i).Nummer == ""
                    Versuche(i).Nummer = "Not found";
                end
                if isempty(Versuche(i).Bauteil) || Versuche(i).Bauteil == ""
                    Versuche(i).Bauteil = "Not found";
                end
                if isempty(Versuche(i).Baustufe) || Versuche(i).Baustufe == ""
                    Versuche(i).Baustufe = "Not found";
                end
                if isempty(Versuche(i).Richtung) || Versuche(i).Richtung == ""
                    Versuche(i).Richtung = "Not found";
                end
            end
            app.Measurement_Database = Versuche;
        end


        %returns Buildstages selected in GUI
        function Builstages_Selected = getBuildstagesfromSelection(app)
            Builstages_Selected = {};
            if app.BS0CheckBox.Value
                Builstages_Selected = [Builstages_Selected, "BS0"];
            end
            if app.BS1CheckBox.Value
                Builstages_Selected = [Builstages_Selected, "BS1"];
            end
            if app.VS1CheckBox.Value
                Builstages_Selected = [Builstages_Selected, "VS1"];
            end
            if app.VS2CheckBox.Value
                Builstages_Selected = [Builstages_Selected, "VS2"];
            end
            if app.ASCheckBox.Value
                Builstages_Selected = [Builstages_Selected, "AS"];
            end
            if app.KEXCheckBox.Value
                Builstages_Selected = [Builstages_Selected, "KEX"];
            end
            if app.FBCheckBox.Value
                Builstages_Selected = [Builstages_Selected, "FB"];
            end
            if app.SERIECheckBox.Value
                Builstages_Selected = [Builstages_Selected, "SERIE"];
            end
            if app.NotfoundCheckBox.Value
                Builstages_Selected = [Builstages_Selected, "Not found"];
            end
        end

        %returns Directions selected in GUI
        function Directions_Selected = getDirectionsfromSelection(app)
            Directions_Selected = {};
            if app.XCheckBox.Value
                Directions_Selected = [Directions_Selected, "-X"];
            end
            if app.XCheckBox_2.Value
                Directions_Selected = [Directions_Selected, "+X"];
            end
            if app.YCheckBox.Value
                Directions_Selected = [Directions_Selected, "-Y"];
            end
            if app.YCheckBox_2.Value
                Directions_Selected = [Directions_Selected, "+Y"];
            end
            if app.ZCheckBox.Value
                Directions_Selected = [Directions_Selected, "-Z"];
            end
            if app.ZCheckBox_2.Value
                Directions_Selected = [Directions_Selected, "+Z"];
            end
        end

        %returns bool vector for filtering Database by selection
        function Selection_Mask = getSelectionMask(app,predict)
            %This function returns a Selction_Mask, an logical array with
            %the length of loaded database, based on the Selctions made at
            %the GUI. The SelectionMask allows to easily filter the
            %Database for the wanted Measurements
            %Initialization of Selection_Mask, which is needed for both
            %selection methods
            Selection_Mask = false(1,length(app.Measurement_Database));
            app.SelectionCell ={};
            app.realPrediction = false;

            %Selection by Tree
            if strcmpi(app.alternativeselectionmethodSwitch.Value,"Off")

                if isempty(app.MeasurementSelection.CheckedNodes)
                    uialert(app.DataAnalysisToolUIFigure,"Please select Data to Process","Error while processing Selection");
                    app.error_ind = true;
                else

                    %get checkedNodes from Checkboxtree
                    checkedNodes = app.MeasurementSelection.CheckedNodes;
                    checkedNodes_Text = strings(length(checkedNodes),1);

                    %writing .Text property of every node into
                    %"checkedNode_Text
                    for i = 1:length(checkedNodes_Text)
                        checkedNodes_Text(i) = checkedNodes(i).Text;
                    end
                    %Filtering the texts for "_" because this only appears at
                    %children nodes
                    checkedNodes_Children = checkedNodes_Text(contains(checkedNodes_Text,"_"));
                    %Writing Modelseries and Year of each children node into
                    %SelectionCell
                    PredictionYearInData = false(length(checkedNodes_Children),1);
                    for i = 1:length(checkedNodes_Children)
                        splittedData = split(checkedNodes_Children(i),"_");
                        app.SelectionCell{i,1}=splittedData(1);%Baureihe
                        app.SelectionCell{i,3}=splittedData(2);%Jahr
                        PredictionYearInData(i) = strcmp(app.SelectionCell{i,3},app.ReferenceYearDropDown.Value);
                    end

                    app.Selected_Buildstages = getBuildstagesfromSelection(app);


                    for i = 1:length(app.SelectionCell(:,1))
                        Selection_Mask =  logical(Selection_Mask + ismember([app.Measurement_Database.Baureihe],app.SelectionCell{i,1})...
                            .* ismember([app.Measurement_Database.Jahr],app.SelectionCell{i,3}));
                    end
                    Selection_Mask = logical(Selection_Mask .* ismember([app.Measurement_Database.Baustufe],app.Selected_Buildstages));
                end

                %selction via alternative method
            else
                %checking if TextField for alternative selection is empty
                if isempty(app.AltSelectionField.Value)
                    uialert(app.DataAnalysisToolUIFigure,"No data input found!","Error while processing selection");
                    app.error_ind = true;
                else
                    %splitting input by ";" to get multiple selection
                    %groups
                    Text_splitted = split(app.AltSelectionField.Value,";");

                    PredictionYearInData = false(length(Text_splitted),1); %Preallocation

                    %searching for attributes in each selection group and
                    %writing them into SelectionCell
                    for i = 1:length(Text_splitted)
                        app.SelectionCell{i,1} = regexp(Text_splitted(i),"[KMAR]+\d+","match"); %Baureihen
                        app.SelectionCell{i,2} = regexp(Text_splitted(i),"KEX|BS\d|FB|VS\d|AS|SERIE","match"); %Baustufen
                        app.SelectionCell{i,3} = regexp(Text_splitted(i),"\d{4}","match"); %Jahre
                        app.SelectionCell{i,4} = regexp(Text_splitted(i),"V\d{6}","match");   %Nummer
                        app.SelectionCell{i,5} = regexp(Text_splitted(i),"GL|VL|GS","match"); %Last

                        PredictionYearInData(i) = contains(app.ReferenceYearDropDown.Value,app.SelectionCell{i,3}{1,1});
                    end

                    Selection_Mask = false(1,length(app.Measurement_Database)); %Preallocation

                    %generating Selection_Mask from SelectionCell by
                    %going through each Selection Group
                    for j = 1:length(app.SelectionCell(:,1)) %loop for Selection Groups
                        Selection_Mask_local = true(1,length(app.Measurement_Database)); %Selection_Mask for current Group

                        %checking for each attribute of Group if empty
                        %otherwise filtering data by attribute
                        if ~isempty(app.SelectionCell{j,1}{1,1})
                            Selection_Mask_local =  and(Selection_Mask_local,ismember([app.Measurement_Database.Baureihe],app.SelectionCell{j,1}{1,1})); end
                        if ~isempty(app.SelectionCell{j,2}{1,1})
                            Selection_Mask_local =  and(Selection_Mask_local,ismember([app.Measurement_Database.Baustufe],app.SelectionCell{j,2}{1,1})); end
                        if ~isempty(app.SelectionCell{j,3}{1,1})
                            Selection_Mask_local =  and(Selection_Mask_local,ismember([app.Measurement_Database.Jahr],app.SelectionCell{j,3}{1,1})); end
                        if ~isempty(app.SelectionCell{j,4}{1,1})
                            Selection_Mask_local =  and(Selection_Mask_local,ismember([app.Measurement_Database.Nummer],app.SelectionCell{j,4}{1,1})); end
                        if ~isempty(app.SelectionCell{j,5}{1,1})
                            Selection_Mask_local =  and(Selection_Mask_local,ismember([app.Measurement_Database.Last],app.SelectionCell{j,5}{1,1})); end

                        %combining Selection_Mask of group with global
                        %Selection_Mask
                        Selection_Mask = or(Selection_Mask,Selection_Mask_local);
                    end
                end
            end

            % erase data from prediction year when predicting
            % (is not equal PredictButton.Value because this used for
            % updateComparisonFiles in Prediction scenarios also)
            % to
            if predict
                Selection_Mask = and(Selection_Mask,~ismember([app.Measurement_Database.Jahr],app.ReferenceYearDropDown.Value));
            end

            % set realPrediction property
            if app.PredictButton.Value; app.realPrediction = true; end

            %Anpassen der Selection_Mask zur Berücksichtugung der gewählten
            %Raumrichtungen
            if ~app.error_ind
                Selected_Directions = getDirectionsfromSelection(app);
                Selection_Mask = and(Selection_Mask,ismember([app.Measurement_Database.Richtung],Selected_Directions));
                if sum(Selection_Mask) == 0 && ~app.PredictButton.Value
                    app.error_ind = true;
                    uialert(app.DataAnalysisToolUIFigure,"No Measurements found for Selection!","Error while processing selection")
                end
            end

            % erase component "Motor" from clusterdata when selected in
            % Settings app
            if app.cluster_woMotor
                Selection_Mask = and(Selection_Mask,~contains([app.Measurement_Database.Bauteil],"Motor"));
            end

        end

        %updates ComparisonFiles shown in DropDown
        function updateComparisonFiles(app,Selection_Mask)
            %Delete any existing entries in the Dropdown of ComparisonFiles
            app.MeasurementFileforComparisonDropDown.Items = string.empty;

            component = lower(app.SelectComponentEditField.Value);
            Comparison_Year = app.ReferenceYearDropDown.Value;

            Comparison_Mask = and(ismember([app.Measurement_Database.Jahr],Comparison_Year),...
                contains(lower([app.Measurement_Database.Bauteil]),component));
            Comparison_Mask = and(Comparison_Mask,Selection_Mask);
            Comparison_Files = app.Measurement_Database(Comparison_Mask);

            if ~app.realPrediction && isempty(Comparison_Files)
                uialert(app.DataAnalysisToolUIFigure,"No Measurement File for Comparison found!","Warning","Icon","warning");
                return
            end

            Comparison_Items = string.empty;

            %limits number of entries to dropdown
            Comparison_Items_IDs = zeros(length(Comparison_Files),1);
            for i = 1:length(Comparison_Items_IDs)
                Comparison_Items(i) = Comparison_Files(i).Dateiname;
                Comparison_Items_IDs(i,1) = Comparison_Files(i).ID;
            end
            app.MeasurementFileforComparisonDropDown.Items     = Comparison_Items;
            app.MeasurementFileforComparisonDropDown.ItemsData = Comparison_Items_IDs;
        end

        %Puts all envelope and members from structData into one array
        function [types, envelopes, members, components, nRowsMems, nRowsEnvs] = LoadDataforCluster(~,structData,Measurement_Names,min_freq,max_freq,freq_steps)

            nColsEnv = ((max_freq - min_freq)/freq_steps)+1 +3; %number of coloums needed for frequencies is ((max-min)/steps +1)...
            %3 additional cols added for: supergroup number, struct number, within struct index

            %Preallocation (was found to be significantly faster for
            %datasets of several thousand entries)
            n=0;
            for s = 1 : size(structData,2)
                for k = 1 : ( size(structData(s).hCluster.AmpEnvelopes,1)-1 )
                    if contains(structData(s).hCluster.grpMembers{k,1},Measurement_Names)
                        n = n+1;
                    end
                end
            end

            envelopes   = zeros(n,nColsEnv);
            members     = cell(n,4);
            types       = string(zeros(size(structData,2),3));
            components  = strings(n,3);

            n = 1;
            for s = 1 : size(structData,2)
                selected_freqs = and((structData(s).hCluster.AmpEnvelopes(end,:) >= min_freq),(structData(s).hCluster.AmpEnvelopes(end,:) <= max_freq));
                for k = 1 : ( size(structData(s).hCluster.AmpEnvelopes,1)-1 )
                    if contains(structData(s).hCluster.grpMembers{k,1},Measurement_Names)
                        members{n,1} = 0;
                        members{n,2} = s;
                        members{n,3} = k;
                        members{n,4} = structData(s).hCluster.grpMembers{k,1};
                        envelopes(n,2)        = s;
                        envelopes(n,3)        = k;
                        envelopes(n,4:end)    = structData(s).hCluster.AmpEnvelopes(k,selected_freqs);
                        components(n,1)       = string(s);
                        components(n,2)       = string(k);
                        components(n,3)       = structData(s).hCluster.components(k);
                        n = n+1;
                    end
                end
            end

            for s = 1 : size(structData,2)
                types(s,1) = 0;
                types(s,2) = s;
                types(s,3) = structData(s).hCluster.type;
            end

            nRowsMems = size(members,1);
            nRowsEnvs = size(envelopes,1);
        end

        %Calculates dist and linkage needed for freq based clustering (hierachical)
        function [sLinkMatrix]  = CalculateDistandLinkage(app,allEnv,distMetric)
            sDistVector = pdist(allEnv(:,4:end),distMetric);
            if any(contains(app.euclidian_metrics,distMetric))
                method = 'ward';
            else
                method = 'average';
            end
            sLinkMatrix = linkage(sDistVector,method);
        end

        %calculates number of superclusters based on linkage calculation
        function [Clusternumber,Clusternumber_idx] = numberOfSuperclusters(app,linkVector,mean_window,sensitivity)
            %determines the number of Clusters to use based on the
            %derivative of the filtered linkageVector
            %linkVector: linkage vector from hierachical clustering
            %mean_window: window to average linkage over

            %creating Vector for Clusternumbers
            nSClstrs = length(linkVector) - (1:length(linkVector))';

            %cfiltering linkVector with mean window
            link_mean = zeros(length(linkVector),1);
            for i = (mean_window+1):length(link_mean)-(mean_window+1)
                link_mean(i) = mean(linkVector(i-mean_window:i+mean_window));
            end

            %derive mean linkage
            mean_link_p = [zeros(mean_window+1,1);diff(link_mean(mean_window+1:end-mean_window-1)); ...
                zeros(mean_window+1,1)];

            %find optimum Clusternumber based on derivative
            Clusternumber_idx = find(mean_link_p > sensitivity,1);
            Clusternumber = nSClstrs(Clusternumber_idx);

            %plot result to figure
            cla(app.LinkagePlotAxes,"reset")
            plot(app.LinkagePlotAxes,nSClstrs,linkVector(:),"k","LineWidth",5);
            xlabel(app.LinkagePlotAxes,"Number of Clusters [-]","FontSize",30);
            ylabel(app.LinkagePlotAxes,"Error in Clusters [-]","FontSize",30);
            title(app.LinkagePlotAxes,"Result of automated number of clusters selection","FontSize",24);
            hold(app.LinkagePlotAxes,"on");
            grid(app.LinkagePlotAxes,"on");
            xlim(app.LinkagePlotAxes,[0 10*Clusternumber]);
            ylim(app.LinkagePlotAxes,[0 link_mean(Clusternumber_idx)*8]);
            xline(app.LinkagePlotAxes,Clusternumber,"r","LineWidth",5);
            text(app.LinkagePlotAxes,Clusternumber+20,link_mean(Clusternumber_idx)+10,append("Selected number of Clusters: ",string(Clusternumber)),...
                "FontSize",30);
            app.NumberofSuperclustersEditField.Value = string(Clusternumber);
        end

        %Clusters frequency data based on calculated linkage (hierachical)
        function [sortedMems,sortedEnvs] = ClusterAndSort(~,allTyp,allMem,allEnv, nRowsMem, nRowsEnv, NsClstr,sLinkMatrix)
            sClstrIdx   = cluster(sLinkMatrix,'MaxClust',NsClstr);

            for i = 1 : nRowsEnv
                allEnv(i,1) = sClstrIdx(i);
            end

            for i = 1 : nRowsMem
                allMem{i,1} = sClstrIdx(i);
            end

            % sort
            sortedEnvs = sortrows(allEnv);
            sortedMems = cell(nRowsMem,4);
            n = 1;
            for i = 1 : NsClstr
                for k = 1 : size(allMem,1)
                    if allMem{k,1} == i
                        sortedMems{n,1} = i;                % supercluster index
                        sortedMems{n,2} = allMem{k,2};      % sub struct index
                        sortedMems{n,3} = allMem{k,3};      % cluster within sub struct index
                        sortedMems{n,4} = allMem{k,4};      % name array
                        n = n+1;
                    end
                end
            end

            sortedTypes = string(zeros(size(allMem,1),size(allTyp,2)));
            for i = 1 : size(allTyp,1)
                for k = 1 : size(sortedTypes,1)
                    if allTyp(i,2) == string(sortedMems{k,2})   % if subcluster indices match...
                        sortedTypes(k,1) = sortedMems{k,1};         % copy the supercluster index, ...
                        sortedTypes(k,2) = sortedMems{k,2};         % the subcluster index...
                        sortedTypes(k,3) = allTyp(i,3);             % and the type
                    end
                end
            end

        end

        %Clusters Envelopes based on Components
        function [srtdEnvs,srtdMems,srtdComps] = ClusterComponents(~,allEnvs,allMems,allComps)
            %Preallocation
            srtdEnvs    = zeros(size(allEnvs));
            srtdMems    = cell(size(allEnvs,1),4);
            srtdComps   = strings(size(allComps,1),4);

            unique_comps = unique(allComps(:,3));

            idx_srt_end = 0;

            for i = 1:length(unique_comps)
                tmp = allComps(:,3) == unique_comps(i); %finding all Envs that origin from component(i)

                idx_srt_bg = idx_srt_end + 1; %setting index for data storage
                idx_srt_end          = idx_srt_end + sum(tmp);

                srtdEnvs(idx_srt_bg:idx_srt_end,2:end)  = allEnvs(tmp,2:end);
                srtdEnvs(idx_srt_bg:idx_srt_end,1)      = i;
                srtdMems(idx_srt_bg:idx_srt_end,2:end)  = allMems(tmp,2:end);
                srtdMems(idx_srt_bg:idx_srt_end,1)      = {i};
                srtdComps(idx_srt_bg:idx_srt_end,2:end) = allComps(tmp,:);
                srtdComps(idx_srt_bg:idx_srt_end,1)     = string(i);
            end
        end

        %general function for envelope generation
        function pE = calculateEnvelope(app,Envs,method)
            %This function calculates the PredictionEnvelope based on the
            %prediction method selected in the GUI and on the Envelopes
            %given to the function
            %
            % pE: predictionEnvelope

            if size(Envs,1) < 2
                pE = Envs;
            else
                % MATLAB implemented methods
                if strcmpi(method,"Maximum");         pE = max(Envs);
                elseif strcmpi(method,"Minimum");     pE = min(Envs);

                    % normal distribution based methods
                elseif strcmpi(method,"Mean");        pE = mean(Envs);
                elseif strcmpi(method,"+1*std.dev.(68%)")

                    pE = mean(Envs) + std(Envs,0,1);
                elseif strcmpi(method,"+2*std.dev.(95%)")
                    pE = mean(Envs) + 2*+ std(Envs,0,1);
                elseif strcmpi(method,"+3*std.dev.(99%)")
                    pE = mean(Envs) + 3*+ std(Envs,0,1);

                % percentiles (total)
                elseif strcmpi(method,"99th-percentile (total)") || strcmpi(method,"95th-percentile (total)") || strcmpi(method,"75th-percentile (total)") ||  strcmpi(method,"Median (total)")
                    N_data = size(Envs,1); % number of selected clusters

                    % calculate magnitude of each Envelope
                    norm_vec = zeros(N_data,1);
                    for i = 1:N_data
                        norm_vec(i) = norm(Envs(i,:));
                    end
                    % sort Envelopes by magnitude
                    [~,idx_vec] = sort(norm_vec); % sort norm_vec in ascending order
                    sEnvs_srtd = Envs(idx_vec,:);  % sort Envs in ascending order

                    switch method
                        case "99th-percentile (total)"; p = 0.99;
                        case "95th-percentile (total)"; p = 0.95;
                        case "75th-percentile (total)"; p = 0.75;
                        case "Median (total)";          p = 0.50;
                    end
                    idx_prctg = floor(N_data*p+1);
                    pE = max(sEnvs_srtd(1:idx_prctg,:),[],1);

                %percentiles (each freq.)
                elseif strcmpi(method,"99th-percentile (each freq.)") || strcmpi(method,"95th-percentile (each freq.)") || strcmpi(method,"75th-percentile (each freq.)") ||  strcmpi(method,"Median (each freq.)")
                    switch method
                        case "99th-percentile (each freq.)"; p = 99;
                        case "95th-percentile (each freq.)"; p = 95;
                        case "75th-percentile (each freq.)"; p = 75;
                        case "Median (each freq.)";          p = 50;
                    end
                pE = prctile(Envs,p,1);

                else
                    uialert(app.DataAnalysisToolUIFigure,"Selected Method for generation of super envelopes not implemented yet!","Error");
                    return
                end
            end
        end

        %Calculates Envelopes of clustering by freqs
        function [sEnvs,sMems] = calculateSuperEnvelopes(app,srtdEnvs,srtdMems,NumberOfSuperClusters,method)
            %creates SuperEnvolopes for each Group by taking the maximum
            %value for each freq
            % additionaly a array with all attributed members is created

            %Preallocation
            sEnvs = zeros(NumberOfSuperClusters,size(srtdEnvs,2)-3);
            sMems = cell(NumberOfSuperClusters,1);

            for sNum = 1:NumberOfSuperClusters
                sEnvs(sNum,:) = calculateEnvelope(app,srtdEnvs(srtdEnvs(:,1)==sNum,4:end),method);

                %cell array with attributed members of each cluster
                sMems{sNum,1} = string(srtdMems([srtdMems{:,1}] == sNum,4));
            end
        end

        %generates prediction for freq based clusters by method selected in GUI
        function [pE,c,CoV_mean] = generatePredictionEnvelope(app,sEnvs,sMems,component,method)
            %This function calculates the PredictionEnvelope based on the
            %prediction method selected in the GUI and on the Envelopes
            %given to the function
            %Additionaly it calculates the average coefficent of deviation
            %of the cluster
            %
            % pE: predictionEnvelope
            % matchidx_loc: bool vector showing for each super envelope if it contains the component
            % sEnvs: double array with Supercluster Envelopes as rows
            % sMems: cell with string array containing the filename of all
            %        Members of each Supercluster
            % component: string of component to predict

            % counts how many times 'component' occurs in sMems
            c = zeros(length(sMems),1);
            for i = 1:length(sMems)
                for j = 1:size(sMems{i,1},1)
                    if contains(lower(sMems{i,1}(j)),component)
                        c(i) = c(i)+1;
                    end
                end
            end
            matchidx_loc = find(c); % outputs the supercluster number of 'component' occurences (loc: local)

            %calculate average coefficent of variation
            [std_env,~] = std(sEnvs(matchidx_loc(:),:),0,1);
            CoV_env = (std_env); %calculate coefficent of variation for each frequency
            CoV_mean = round(mean(CoV_env),1);

            if length(matchidx_loc) > 1
                pE = calculateEnvelope(app,sEnvs(matchidx_loc(:),:),method);
            else
                pE = sEnvs(matchidx_loc,:);  % if there is only one match, the above is not executed
            end
        end

        %Converts Mems form cell to string array and extracts components
        function [selectedMems,selectedComps] = convertMembers(~,sMems,componentInEnvs)
            sMems_filt = sMems(componentInEnvs > 0,:);
            selectedMems = strings(1,length(sMems_filt));
            selectedComps = strings(1,length(sMems_filt));

            for i = 1:size(sMems_filt,1)
                selectedMems(1,i) = i;
                selectedComps(1,i)= i;
                for j = 2: size(sMems_filt{i},1)+1
                    selectedMems(j,i) = sMems_filt{i}(j-1);
                    exp = "(?:[KMAR]+\d*)_?(?>\sMUE2|MÜ_Funtionsba_-|-20|_-|_TUE)*_*(?:V?\d{6})?_\d\d\.\d\d\.(?:\d{4})_(?<Bauteil>.+)_(?:[\+-][XYZ])?S?_(?:GL|VL|GS)[_-]HL_(?:\d)";
                    tmp = regexp(selectedMems(j,i),exp,"names","once");
                    selectedComps(j,i) = tmp.Bauteil;
                end
            end
        end

        %Exports given ClusterData to Excelfile
        function exportDatatoExcel(app,Mems,Envs,Comp,pE,filename)
            %Info
            InfoData = calculateInfoData(app,Envs,Comp,pE);
            writematrix(["Group Number", "Number of selected Component in Cluster" ,...
                "Distance to SuperEnvelope", "Distance Envelope of Comparison Files"],filename,"Sheet","Info");
            writematrix(InfoData,filename,"Sheet","Info","Range","A2");
            %Members
            writematrix(["Group Number";"Files in Group"],filename,"Sheet","Members");
            writematrix(Mems,filename,"Sheet","Members","Range","B1");
            %Envelopes
            Env_header = transpose(["Frequenzen [Hz]","SuperEnvelope","Comparison Envelope",append("Group ",Mems(1,:))]);
            writematrix(Env_header,filename,"Sheet","Envelopes");
            freqs = app.min_freq:app.freqres:app.max_freq;
            writematrix(freqs,filename,"Sheet","Envelopes","Range","B1");
            writematrix(pE,filename,"Sheet","Envelopes","Range","B2");
            writematrix(app.pE_Comparison,filename,"Sheet","Envelopes","Range","B3")
            writematrix(Envs,filename,"Sheet","Envelopes","Range","B4");
            %Components
            writematrix(["Group Number"; "Components in Group"],filename,"Sheet","Components");
            writematrix(Comp,filename,"Sheet","Components","Range","B1");
        end

        function InfoData = calculateInfoData(app,Envs,Comps,pE)
            InfoData = zeros(size(Comps,2),2);

            c = zeros(size(Comps,2),1);
            for i = 1:size(Comps,2)
                InfoData(i,1) = i;
                for j = 1:size(Comps,1)
                    if contains(Comps(j,i),app.SelectComponentEditField.Value)
                        c(i) = c(i)+1;
                    end
                end
            end
            InfoData(:,2) = c;

            if ~app.realPrediction
                dist2Env  = zeros(size(Envs,1),1);
                dist2Comp = zeros(size(Envs,1),1);
                for i = 1:size(Envs,1)
                    dist2Env(i)  = pdist([Envs(i,:);pE]);
                    dist2Comp(i) = pdist([Envs(i,:);app.pE_Comparison]);
                end
                InfoData(:,3) = dist2Env;
                InfoData(:,4) = dist2Comp;
            end
        end

        function Filename = generateFilename(app,baseName, fileExtension)
            c = fix(clock);
            timestamp = append(string(c(1)),"-",sprintf('%02d',c(2)),"-",sprintf('%02d',c(3)),"--"...
                ,sprintf('%02d',c(4)),"-",sprintf('%02d',c(5)));
            Filename_woPath = append(baseName,"_Comp-",app.SelectComponentEditField.Value,...
                "_RefYear-",app.ReferenceYearDropDown.Value,"_Methd-",string(app.predictMthd),"_",timestamp,fileExtension);
            Filename = append(app.file_path,'\',Filename_woPath);
        end

        function exportDataToMatlab(app,Mems,Envs,Comp,pE,filename)
            %Info
            InfoData = calculateInfoData(app,Envs,Comp,pE);
            InfoHeader = ["Group Number", "Number of selected Component in Cluster" ,...
                "Distance to SuperEnvelope", "Distance Envelope of Comparison Files"];
            %Members
            MemsHeader = ["Group Number";"Files in Group"];
            %Envelopes
            EnvsHeader = transpose([append("Group ",Mems(1,:))]);
            freqs = app.min_freq:app.freqres:app.max_freq;
            pE_Comparison = app.pE_Comparison;
            %Components
            CompHeader = ["Group Number"; "Components in Group"];

            %Export
            save(filename,...
                "InfoHeader","InfoData","CompHeader","Comp","EnvsHeader","Envs","MemsHeader","Mems","pE","pE_Comparison","freqs");
        end

        function trans_tab = CoG_TranslationTable(app)
            trans_tab = cell(1);
            % {i,1}: Strings in CoG-Daten    {i,2}: Strings in Messdaten
            trans_tab{1,1} = ["Batterie (Blei)"];   trans_tab{1,2} = ["Batterie"];
            trans_tab{end+1,1} = ["Blinker / FIBL"];    trans_tab{end,2} = [ "Blinker_h_l","Blinker_h_r","Blinker_hi_li",...
                "Blinker_hi_re","Blinker_v_l","Blinker_v_r","Blinker_vo_li",...
                "Blinker_vo_re""Blinker_LH_o_A", "Blinker_RH_o_A",...
                "Blinker_hi_li","Blinker_hi_re","Blinker_vo_li","Blinker_vo_re"];
            trans_tab{end+1,1} = ["Federung Hinten"]; trans_tab{end,2} = ["FB_H_o","FB_H_u","FB_hi_ob_Ant","FB_hi_un_Ant",...
                "Federb_hi_Ant_o","Federb_hi_Ant_u","Federb_hi_Ausgl"];
            trans_tab{end+1,1} = ["Frontträger"]; trans_tab{end,2} = ["FrontTr_l_u","FrontTr_r_u","Frontr_Ant_o","Frontr_Ant_o"...
                ,"Frontr_Ant_u","Fronttr_Antw_ob","Fronttr_Antw_u"];
            trans_tab{end+1,1} = ["HECU"]; trans_tab{end,2} = ["Hecu","Hecu Anb","Hecu2","Hecu_A","Hecu_Anb",...
                "Hecu_StG_Deck_re","Hecu","Hecu Anb","Hecu_A","Hecu_Anb","Hecu_u_Anb"];
            trans_tab{end+1,1} = ["Heckleute"]; trans_tab{end,2} = ["Heckl_Anb","Heckl_Ant","Heckl_oben"];
            trans_tab{end+1,1} = ["HRM"]; trans_tab{end,2} = ["HeckR_re_vo_ob","HeckRa_RAP_L",...
                "HeckRa_RAP_R","HeckRa_RAP_l","HeckRa_RAP_r","HeckRa_l_m_o","HeckRa_l_m_u","HeckRa_l_o_A","HeckRa_l_u_A",...
                "HeckRa_r_m_o","HeckRa_r_m_u","HeckRa_r_o_A","HeckRa_r_u_A","Heckr_RAP_li","Heckr_RAP_re","Heckr_li_hi","Heckr_re_hi"...
                ,"HeckRa_RAP_l","HeckRa_RAP_r","HeckRa_l_o_A","HeckRa_r_o_A","Heckr_RAP_li","Heckr_RAP_re","Heckr_li_mi_o","Heckr_li_mi_ob"...
                ,"Heckr_re_hi","Heckr_re_mit_ob","Heckr_re_mit_u","Heckr_re_vo_ob","Heckr_re_vo_u","Heckr_li_vo_o","Heckr_li_vo_ob"...
                ,"Heckr_li_vo_u","Heckr_re_mi_o","Heckr_re_mi_ob","Heckr_re_vo_o","Heckr_re_vo_ob","Heckr_re_vo_u"];
            trans_tab{end+1,1} = ["I-Kombi"]; trans_tab{end,2} = ["I-Kombi","I-Kombi_ob"];
            trans_tab{end+1,1} = ["Kennzeichenträger"]; trans_tab{end,2} = ["KennzTr_l_o_A","KennzTr_r_o_A","KennzTräger"];
            trans_tab{end+1,1} = ["Kennzeichnenleuchte"]; trans_tab{end,2} = ["KennzL_m","KennzLeuchte","KennzLeuchte_Anb","KennzLeuchte"];
            trans_tab{end+1,1} = ["Keylessride"]; trans_tab{end,2} = ["KeylRide_Anb_GP","KeylRide_Anb_Tr","KeylRide_Anb_li",...
                "KeylRide_Anb_re","KeylRide_GrPl_li","KeylRide_GrPl_re","KeylRide_ob_hi","KeylRide_ob_vo","Keyl_Anb_rs_li",...
                "Keyl_Ant_o_hi","Keyl_Ant_o_vo","Keyl_GrPl_li","Keyl_GrPl_re","Keyl_Halter_li_o","Keyl_Halter_li_u",...
                "Keyl_Ride_Anb","Keyl_Ride_Ant","Keyl_Ride_Ant_Gr","Keyl_Ride_Ant_ob"];
            trans_tab{end+1,1} = ["Kofferträger"]; trans_tab{end,2} = ["Koffer_Anb_li","Koffer_Anb_re"];
            trans_tab{end+1,1} = ["Lenkerarmaturen"]; trans_tab{end,2} = ["LKR-Arma_L","LKR-Arma_R","LKR_Arma_l","LKR_Arma_r","Lenker_Arma_li",...
                "Lenker_Arma_re"];
            trans_tab{end+1,1} = ["Lenkergrundplatte"]; trans_tab{end,2} = ["LKRGrPl_m""LenkerGrPl","LenkerGrPl_2","LenkerGrPl_mi","Lenker_Gr_Pl","LenkerGrPl","Lenkergrdpl"];
            trans_tab{end+1,1} = ["Motor"]; trans_tab{end,2} = ["Motor","Motor2"];
            trans_tab{end+1,1} = ["SAF-Slave"]; trans_tab{end,2} = ["SAF"];
            trans_tab{end+1,1} = ["Scheinwerfer"]; trans_tab{end,2} = ["SW_Ant_li","SW_Ant_re","SW_l","SW_r","SW_Anb_li"...
                ,"SW_Anb_li_o","SW_Anb_li_u","SW_Anb_re","SW_Anb_re_o","SW_Anb_re_u","SW_Antw_li","SW_Antw_re","SW_Geh_Ant_li",...
                "SW_Geh_Ant_re","SW_LED_Steuerg","Scheinw_Anb_li","Scheinw_Anb_re","Scheinw_Geh_hi","Scheinw_Geh_ob"];
            trans_tab{end+1,1} = ["Seitenstützenschalter"]; trans_tab{end,2} = ["SSS"];
            trans_tab{end+1,1} = ["Sensorbox"]; trans_tab{end,2} = ["Sensorbox","Sensorbox_Anb","Sensorbox_Ant",...
                "Sensorbox_Integr","Sensorbox_innen","Sensorbox_l_A","Sensorbox_r_A","Sensorbox_Anb_al","Sensorbox_Ant"...
                ,"Sensorbox_Ant_ne","Sensorbox_Integr","Sensorbox_Steck","Sensorbox_innen","Sensorbox_li_Anb","Sensorbox_r_A","Sensorbox_re_Anb","SB_Aufn_Fahrer_h"...
                ,"SB_Aufn_Fahrer_v","SB_Aufn_Sozius_h","SB_Aufn_Sozius_v","Sensorbox_Anb","Sensorbox_Ant","Sensorbox_Antw"];
            trans_tab{end+1,1} = ["Steuerkopf"]; trans_tab{end,2} = ["Steuerkopf","Steuerkopf ob","Steuerkopf_o",...
                "Steuerkopf_ob","Steuerkopf_u","Steuerkopf_un","Steuerkopf_unt"];
            trans_tab{end+1,1} = ["SwiLa Links und Rechts"]; trans_tab{end,2} = ["SchwiLa_L","SchwiLa_R","SchwiLa_l",...
                "SchwiLa_r","SchwingenL_li","SchwingenL_re","Schwingenlager_r","SchwiLa_l","SchwiLa_r","Schwingenl_li","Schwingenl_re","Schwingenl_li","Schwingenl_re"];
            trans_tab{end+1,1} = ["Seitenstützenschalter"]; trans_tab{end,2} = ["Seitenst_Schalt"];
            trans_tab{end+1,1} = ["Tank"]; trans_tab{end,2} = ["Tank_h_A","Tankdeckel","Tank_Anb_hi","Tank_Anb_vo_li","Tank_Anb_vo_re","Tank_Anbind_hi","Tank_Anb_vo_li"...
                ,"Tank_Anb_vo_re","Tank_Anbind_hi","Tankdeckel"];
            trans_tab{end+1,1} = ["Zundlenkschloss"]; trans_tab{end,2} = ["ZLS","ZLS_A","ZLS_r_A","ZLS Anb","ZLS_Anb","ZLS_Ant_GrPl","ZLS_Ant_Seite"];
        end

        function [srtdEnvs,srtdMems] = ClusterCoGbased(app,Envs,Mems,Comps)
            %1. jeder Komponente/Hüllkurve CoG-Daten zuordnen anhand von
            %Übersetzungstabelle
            app.trans_tab = CoG_TranslationTable(app); %Übersetzungstabelle laden

            % Vektor mit übersetzen Komponenten erzeugen
            Comps_trans = strings(length(Comps),1);
            for i = 1:length(Comps(:,3))
                for j = 1:length(app.trans_tab)
                    if contains(Comps(i,3),app.trans_tab{j,2})
                        Comps_trans(i) = app.trans_tab{j,1};
                        break
                    end
                end
            end
            %2. CoG Daten für jede Komponente ermitteln
            % Baureihe der Messungen wird aus Mems mit Regular Expression
            % ermittelt
            exp = "^[KMAR]+\d*"; %Regular Expression zur Ermittlung der Baureihe
            CoGs = zeros(length(Comps),3);
            CoGs_valid = true(length(Comps),1); %boolean vector für fehlende Komponentenübersetzung

            for i = 1:length(Comps)
                if Comps_trans(i) == "" %fehlende Komponentenübersetzung abfangen
                    CoGs_valid(i) = false;
                    continue
                else
                idx_BS = contains([app.CoGfiles.Baureihe],regexp(Mems{i,4},exp,"match")); %Baureihe identifizieren
                %CoG aus CoG files zuordnen
                CoGs(i,:) = app.CoGfiles(idx_BS).CoGs(contains([app.CoGfiles(idx_BS).parts],Comps_trans(i)),:);

                % Scale Buildseries with wheelbase
                if ~isempty(app.Wheelbase{1,1})
                    WB_idx = strcmp(string(app.Wheelbase(:,1)),app.CoGfiles(idx_BS).Baureihe);
                    WB = app.Wheelbase{WB_idx,2};
                    CoGs(i,:) = CoGs(i,:)/WB;

                end

                %Baureihe als Prefix fürs später Plotten vor
                %Komponentennamen
                Comps_trans(i) = append(Comps_trans(i)," (",app.CoGfiles(idx_BS).Baureihe,")");
                end
            end

            fprintf(append("Found ",string(sum(CoGs_valid))," Datasets with valid CoGs",newline))

            %Clustern nach ausgewählter Methode
            if app.method_CoG == "hierachical"
                DistVec = pdist(CoGs(CoGs_valid,:),"euclidean");
                LinkMatrix = linkage(DistVec);
                app.ClstrIdx_CoG = cluster(LinkMatrix,"maxclust",app.NCoGClusters);
            elseif app.method_CoG == "kMeans"
                app.ClstrIdx_CoG = kmeans(CoGs(CoGs_valid,:),app.NCoGClusters,"Display","final");
            else
                error("Selected Clustermethod for pos. based Clustering not implemented yet!")
            end

            %Plotten der gebildeten Cluster
            hold(app.CoGPositionsAxes,"on")
            title(app.CoGPositionsAxes,"CoG of all Components")
            app.CoGs_real = CoGs(CoGs_valid,:);
            app.Comps_trans_real = Comps_trans(CoGs_valid);
            ico_list = ["o","+","*",".","x","_","|","s","d","^","<",">"];
            for i = 1:app.NCoGClusters
                scatter(app.CoGPositionsAxes,app.CoGs_real(app.ClstrIdx_CoG == i,1),app.CoGs_real(app.ClstrIdx_CoG == i,3),48,ico_list(randi(12)));
                CoG_txt = app.CoGs_real(app.ClstrIdx_CoG == i,:);
                Comp_txt = app.Comps_trans_real(app.ClstrIdx_CoG== i);
                [~,ia,~] = unique(Comp_txt);
                text(app.CoGPositionsAxes,CoG_txt(ia,1),CoG_txt(ia,3),append("  ",Comp_txt(ia)));
            end

            xlabel(app.CoGPositionsAxes,"scaled X [-]"); ylabel(app.CoGPositionsAxes,"scaled Y [-]");
            app.CoGPositionsAxes.Visible = "on";

            %Daten ohne CoG aus Vektoren entfernen
            Envs_real = Envs(CoGs_valid,:);
            Mems_real = Mems(CoGs_valid,:);

            Envs_real(:,1) = app.ClstrIdx_CoG;
            Mems_real(:,1) = num2cell(app.ClstrIdx_CoG);

            % sort
            srtdEnvs = sortrows(Envs_real);
            srtdMems = cell(length(Mems_real),4);
            n = 1;
            for i = 1 : app.NCoGClusters
                for k = 1 : size(Mems_real,1)
                    if Mems_real{k,1} == i
                        srtdMems{n,1} = i;                   % supercluster index
                        srtdMems{n,2} = Mems_real{k,2};      % sub struct index
                        srtdMems{n,3} = Mems_real{k,3};      % cluster within sub struct index
                        srtdMems{n,4} = Mems_real{k,4};      % name array
                        n = n+1;
                    end
                end
            end
        end

        function plotClusters(~,PlotAxes,freqs,sEnvs,pE,color)
            cla(PlotAxes,"reset")
            hold(PlotAxes,"on")

            for i = 1:size(sEnvs,1)
                if i == 1
                    plot(PlotAxes,freqs,sEnvs(i,:),"-","Color",[0.3 0.3 0.3],"DisplayName","Envelopes")
                else
                    plot(PlotAxes,freqs,sEnvs(i,:),"-","Color",[0.3 0.3 0.3],"HandleVisibility","off")
                end
            end
            plot(PlotAxes,freqs,pE,"Color",color,"LineWidth",5,"DisplayName","Prediction");

            xlabel(PlotAxes,'frequency [Hz]');
            ylabel(PlotAxes,'acceleration [m/s^2]');
            grid(PlotAxes,"on");
            set(PlotAxes,"FontSize",26)
            legend(PlotAxes,"Location","northeast")
            PlotAxes.Visible = "on";
        end

        function [sortedMems,sortedEnvs, sortedTypes, sDist,s_idx] = ClusterAndSort_kMeans(~,allTyp,allMem,allEnv, nRowsMem, nRowsEnv, NsClstr,distMetric)
            %sClusterAndSort takes input data and clusters... and sorts
            %   "s" stands for "super" as in supercluster

            disp("Clustering and sorting.")

            % cluster
            %clustering with kMeans Method
            sDist = allEnv(:,4:end);
            rng("default");
            s_idx = kmeans(sDist,NsClstr,"Display","final","Replicates",1,"Distance",distMetric);


            for i = 1 : nRowsEnv
                allEnv(i,1) = s_idx(i);
            end

            for i = 1 : nRowsMem
                allMem{i,1} = s_idx(i);
            end

            % sort
            disp("Sorting envelopes...")
            sortedEnvs = sortrows(allEnv);

            disp("Sorting members...")
            sortedMems = cell(nRowsMem,4);
            n = 1;
            for i = 1 : NsClstr
                for k = 1 : size(allMem,1)
                    if allMem{k,1} == i
                        sortedMems{n,1} = i;                % supercluster index
                        sortedMems{n,2} = allMem{k,2};      % sub struct index
                        sortedMems{n,3} = allMem{k,3};      % cluster within sub struct index
                        sortedMems{n,4} = allMem{k,4};      % name array
                        n = n+1;
                    end
                end
            end
            disp("Sorting types...")
            sortedTypes = string(zeros(size(allMem,1),size(allTyp,2)));
            for i = 1 : size(allTyp,1)
                for k = 1 : size(sortedTypes,1)
                    if allTyp(i,2) == string(sortedMems{k,2})   % if subcluster indices match...
                        sortedTypes(k,1) = sortedMems{k,1};         % copy the supercluster index, ...
                        sortedTypes(k,2) = sortedMems{k,2};         % the subcluster index...
                        sortedTypes(k,3) = allTyp(i,3);             % and the type
                    end
                end
            end
            disp("Finished clustering.")
        end

        function PlotCoGsFreqClstComparison(app,component)

            %add all Members of position based list to a single string
            %array
            for i = 1:length(app.sMemsCoG)
                if i == 1
                    sMemsCoGarray = app.sMemsCoG{1};
                else
                    sMemsCoGarray = [sMemsCoGarray ; app.sMemsCoG{i}];
                end
            end

            %compInfreqCluster = strings(1); %string array in which all components of CoG based clustering that appear in the freq based Cluster are noted

            %loop through selected Members of freq based Clustering to get
            %component in freq based Cluster
            for i = 1:size(app.selectedMems_freq,2)
                MemsInCoGData = contains(app.selectedMems_freq(2:end,i),sMemsCoGarray);
                if ~exist("compInfreqCluster","var")
                    compInfreqCluster = app.selectedComp_freq([false; MemsInCoGData],i);
                else
                    compInfreqCluster = [compInfreqCluster ; app.selectedComp_freq([false; MemsInCoGData],i)];
                end
            end

            %Vector with all components also contained in freq based
            %Cluster
            %compInfreqCluster = unique(compInfreqCluster);

            %filter single occurences
            [GC,CompGroups] =groupcounts(compInfreqCluster);
            compInfreqCluster = CompGroups(GC > 3);

            %translate vector to CoG Names
            CompsInfreq_trans = strings(length(compInfreqCluster),1);
            for i = 1:length(CompsInfreq_trans)
                for j = 1:length(app.trans_tab)
                    if contains(compInfreqCluster(i),app.trans_tab{j,2})
                        CompsInfreq_trans(i) = app.trans_tab{j,1};
                        break
                    end
                end
            end

            CompsInfreq_trans = unique(CompsInfreq_trans);

            %create Plot
            cla(app.CoGPositionsAxes,"reset")
            hold(app.CoGPositionsAxes,"on")
            ylabel(app.CoGPositionsAxes,"scaled Y [-]")
            xlabel(app.CoGPositionsAxes,"scaled X [-]")
            title(app.CoGPositionsAxes,"CoG of all Components")
            ico_list = ["o","+","*",".","x","_","|","s","d","^","<",">"];
            set(app.CoGPositionsAxes,'DataAspectRatio',[1 1 1])
            if app.NCoGClusters < 13
                clst_icons = ico_list(randperm(12,app.NCoGClusters));
            else
                clst_icons = ico_list(randi(12,app.NCoGClusters,1));
            end

            [CompTrans_unique,ia,~] = unique(app.Comps_trans_real);

            %Loop through all components
            for i = 1:length(CompTrans_unique)
                scatter(app.CoGPositionsAxes,app.CoGs_real(ia(i),1),app.CoGs_real(ia(i),3),48,"k",clst_icons(app.ClstrIdx_CoG(ia(i))));
                CoG_txt = app.CoGs_real(ia(i),:);
                Comp_txt = app.Comps_trans_real(ia(i));
                if contains(Comp_txt,component)
                    text(app.CoGPositionsAxes,CoG_txt(1),CoG_txt(3),append("  ",Comp_txt),"FontWeight","bold","Color","r");
                elseif contains(Comp_txt,CompsInfreq_trans)
                    text(app.CoGPositionsAxes,CoG_txt(1),CoG_txt(3),append("  ",Comp_txt),"Color","r");
                else
                    text(app.CoGPositionsAxes,CoG_txt(1),CoG_txt(3),append("  ",Comp_txt));
                end
            end
        end

        function [magnErr_str,anglErr_str] = calculateErrors(app,pE_Comparison,pE)
            errVec  = [pE_Comparison; pE]; % build error vector
            % Magnitude Error
            magnErr = round(app.freqres*sum(abs(errVec(2,:) - errVec(1,:)))/1000,0); % in Hz*m/s^2
            % Conformitiy of Shape
            anglErr = round(1- pdist(errVec,'cosine'),3); % 'cosine' returns 1-cos(phi)
            %convert to strings
            magnErr_str = string(magnErr);
            anglErr_str = string(anglErr);
        end
    end


    % Callbacks that handle component events
    methods (Access = private)

        % Code that executes after component creation
        function startupFcn(app)
            clc

            % change matlab working dir to path of app
            full_file_path = mfilename('fullpath');
            [app.file_path , ~ , ~] = fileparts(full_file_path);
            addpath(app.file_path)

            % check if Statistics and Maschine Learning Toolbox is
            % installed and enabled
            addons = matlab.addons.installedAddons;
            idx_STML = contains(addons{:,"Name"},"Statistics and Machine Learning Toolbox");
            if ~any(idx_STML) || ~addons{idx_STML,"Enabled"}
                warning("Statistics and Maschine Learning Toolbox was not found! Please make sure it is installed, because it is used within this app.");
                uialert(app.DataAnalysisToolUIFigure,"Statistics and Maschine Learning Toolbox was not found! Please make sure it is installed, because it is used within this app.","Toolbox missing!");
            end
        end

        % Button pushed function: SetupButton
        function SetupButtonPushed(app, event)
            f = uiprogressdlg(app.DataAnalysisToolUIFigure,"Title","Running Setup",...
                "Message","Reading GUI Input..."); f.Value = 0.1;
            a = app.MeasurementSelection.Children;
            a.delete;

            %% load and process CoG-data
            app.CoGfiles  = dir(append(app.file_path,'\**\Schwerpunktdaten'));
            app.CoGfiles = app.CoGfiles(~[app.CoGfiles.isdir]);
            app.CoGfiles = rmfield(app.CoGfiles,["date","bytes","isdir","datenum"]);

            for i = 1:length(app.CoGfiles)
                % Read file Radstände
                if strcmp(app.CoGfiles(i).name,'Radstände.csv')
                    app.Wheelbase = readcell(append(app.CoGfiles(i).folder,"\",app.CoGfiles(i).name));
                    if strcmp(app.Wheelbase{1,1},'Baureihe') %remove first line from cell
                        app.Wheelbase = app.Wheelbase(2:end,:); end
                    continue
                end

                app.CoGfiles(i).Baureihe = string(erase(app.CoGfiles(i).name,'.csv'));
                tmp_CoGdata_raw = importdata(append(app.CoGfiles(i).folder,"\",app.CoGfiles(i).name));
                raw_parts = convertCharsToStrings(tmp_CoGdata_raw.textdata(2:end,1));
                raw_CoGs  = tmp_CoGdata_raw.data;

                [app.CoGfiles(i).parts,~,Comps_idx] = unique(raw_parts,'stable');

                %mitteln der CoGs für Bauteile mit mehreren Componenten
                app.CoGfiles(i).CoGs = zeros(length(app.CoGfiles(i).parts),3);
                for j = 1:length(app.CoGfiles(i).parts)
                        app.CoGfiles(i).CoGs(j,:) = mean(raw_CoGs(Comps_idx == j,:),1);
                end

                %CoG des Schwingenlagers für Transformation bestimmen
                CoG_SwiLa = app.CoGfiles(i).CoGs(contains(app.CoGfiles(i).parts,"SwiLa Links und Recht"),:);
                %Transformation ins Schwingen KOS
                app.CoGfiles(i).CoGs = app.CoGfiles(i).CoGs - CoG_SwiLa;
            end

            %% update frequency range
            updateSelectedFrequencies(app);

            %% Process measurement data
            app.faultyData = cell({});

            app.readPaths = dir(append(app.file_path,'\**\3_Peak*'));

            %checking if data data is found in the given path
            if isempty(app.readPaths)
                uialert(app.DataAnalysisToolUIFigure,append("Not data found!",newline,"Please review the datapath."),"Error during Setup");
            else
                f.Value = 0.2; f.Message = "Creating Database...";
                CreateDatabase(app);
                Modelseries = unique([app.Measurement_Database.Baureihe]);
                f.Value = .75; f.Message = "Updating Selection Tree..";

                % create CheckboxTree
                app.treenodes = cell(length(Modelseries),1);
                Modelseries_all = [app.Measurement_Database.Baureihe];
                for i = 1: length(Modelseries)
                    app.treenodes{i}{1} = uitreenode(app.MeasurementSelection,"Text",Modelseries(i));
                    YearsOfModelseries = unique([app.Measurement_Database(ismember(Modelseries_all,Modelseries(i))).Jahr]);
                    for j = 2: length(YearsOfModelseries)+1
                        app.treenodes{i}{j}=uitreenode(app.treenodes{i}{1},"Text",append(Modelseries(i),"_",YearsOfModelseries(j-1)));
                    end
                end
            end
            f.Value = 1; f.Message ="Finished";
            close(f)
        end

        % Button pushed function: DataPreparationButton
        function ButtonDataPreparationPushed(app, event)
            %Selection if all data reloaded or only missing data isprocessed
            selection = uiconfirm(app.DataAnalysisToolUIFigure,"Do you want to update all data or add new data?",...
                "Select Data perparation Mode",'Options',{'All data','New data','Cancel'},...
                'DefaultOption',2,'CancelOption',3);
            switch selection
                case 'All data'
                    app.addData = false;
                case 'New data'
                    app.addData = true;
                case 'Cancel'
                    return
            end

            %output warning when, app.readpath is empty
            if isempty(app.readPaths)
                uialert(app.DataAnalysisToolUIFigure,...
                    "Please make sure Setup is run prior and read- and save-path are set correctly!",...
                    "Warning","Icon","warning")
                return
            end

            %frequency selection for data import
            min_freq_data = 4;
            max_freq_data = 3200;
            freqres_data = 4;
            spectr_data = [min_freq_data, max_freq_data];
            loIndex_data = spectr_data(1)/freqres_data;
            fSteps_data = (spectr_data(2)-spectr_data(1))/freqres_data;

            nc = 1;

            %start progress bar on GUI
            f = uiprogressdlg(app.DataAnalysisToolUIFigure,"Title","Data Preparation");
            f.Value = 0.1; f.Message = "Starting data preparation...";

            for i = 1 : length(app.readPaths)
                %step progress bar
                f.Value = 0.1 + i*0.9/length(app.readPaths);
                f.Message = append("Processing Folder ", string(i)," out of ",string(length(app.readPaths)));


                fPath = dir(append(app.readPaths(i).folder,'\', app.readPaths(i).name,'\**\K*.txt')); %current file path
                sPath = append(app.readPaths(i).folder,'\4_Hüllkurven');                   %current save path

                if size(fPath,1) == 0
                    continue   % if directory is empty, skip entirely
                end

                saveName    = app.readPaths(i).folder;
                saveName    = split(saveName,'\ab ');
                saveName    = replace(saveName,'\','_');
                type        = saveName;
                type        = type{2,1};
                saveName    = append(saveName(2,1),'.mat');

                if isfile(append(sPath,'\',saveName{1})) && app.addData
                    continue
                end

                Database_Folder = app.Measurement_Database([app.Measurement_Database.Pfad] == app.readPaths(i).folder);

                [names,data,components,~,falseData]      = ReadData(app,fPath,Database_Folder);
                amplEnv = [squeeze(data(loIndex_data:loIndex_data+fSteps_data,2,:)),...
                    squeeze(data(loIndex_data:loIndex_data+fSteps_data,1,1))]';
                members = cellstr(names');
                nc = nc+1;
                app.faultyData{i,1} = falseData;

                hCluster    = struct('type',[],'AmpEnvelopes',[],'grpMembers',[]);

                hCluster.type            = type;
                hCluster.AmpEnvelopes    = amplEnv;
                hCluster.grpMembers      = members;
                hCluster.components      = components;

                %SAVE FILE
                if ~exist(sPath, 'dir'); mkdir(sPath); end % create folder if not existing
                % do NOT change name 'hCluster'!
                save(append(sPath,'\',saveName{1}),'hCluster');
            end
            f.Value = 1; f.Message = "Finished";
            clear amplEnv members type expData N_clstr NameArray names nbrFiles saveName sPath data fPath
            close(f)
        end

        % Button pushed function: ClusterButton
        function ClusterButtonPushed(app, event)
            f = uiprogressdlg(app.DataAnalysisToolUIFigure,"Title","Clustering");

            %% reset
            f.Value = 0.1; f.Message = "Resetting Plots...";
            %resetting properties containing envelopes and corresponing
            %members of clusters
            [app.sEnvs_freq, app.sMems_freq] = deal({},{});
            [app.sEnvsC,app.sMemsC] = deal({},{});
            [app.sEnvsCoG,app.sMemsCoG] = deal({},{});
            %restting error index
            app.error_ind = false;
            % reset bool var that decided if data for CoG clustering is
            % available in selection
            app.CoGCluster_valid = false;
            %resetting plots
            cla(app.Axes_Predicted_Envelopes,'reset');
            cla(app.CoGPositionsAxes,'reset')
            cla(app.componentbasedClustersAxes,'reset')
            cla(app.freqClustersAxes,'reset')
            cla(app.positionbasedClustersAxes,'reset')

            %hide all axes of individual cluster methods
            app.Axes_Predicted_Envelopes.Visible = "off";
            app.componentbasedClustersAxes.Visible = "off";
            app.freqClustersAxes.Visible = "off";
            app.positionbasedClustersAxes.Visible = "off";
            app.CoGPositionsAxes.Visible = "off";

             %Delete any existing entries in the Dropdown of ComparisonFiles
            app.MeasurementFileforComparisonDropDown.Items = string.empty;

            % reset error text fields
            [app.MagnitudeerrorTextArea.Value, app.ShapeerrorTextArea.Value] = deal("","");
            [app.componentbased_Mag.Value, app.componentbased_Shape.Value] = deal("","");
            [app.positionbased_Mag.Value, app.positionbased_Shape.Value] = deal("","");

            clc;

            %% initialize clustering
            %get Number of Superclusters for Clustering from GUI
            app.NumberOfSuperClusters = str2double(app.NumberofSuperclustersEditField.Value);

            f.Value = .2; f.Message = "Processing Selection...";
            %Get SelectionMask from function
            Selection_Mask = getSelectionMask(app,app.PredictButton.Value);

            %abort clustering when error occurred during selection Mask
            %generation
            if app.error_ind; return; end

            fprintf(append("Found ",string(sum(Selection_Mask))," Measurements for Clustering",newline))

            if sum(Selection_Mask) > 15000 && app.frequencybasedCheckBox.Value
                selection = uiconfirm(app.DataAnalysisToolUIFigure,...
                    append("You selected more than 15,000 files and the frequency based clustering method!", ...
                    newline,"Clustering will likely take more than 5 min and will require large portions of RAM.",...
                    newline,"Do you want to proceed the clustering?"),...
                    "Warning on selected Clustering",'Options',{'Yes. Proceed','Cancel'},...
                    'DefaultOption',2,'CancelOption',2);
                switch selection; case 'Cancel'; return; end
            end

            %Selection of Measurements from Measurement Database by selection mask
            Selected_Measurements = app.Measurement_Database(Selection_Mask);
            estmdTime = round(8.35e-11*length(Selected_Measurements)^3,0); % estimation based on experiments made with freq. range 72-2000 Hz

            f.Value = .6;
            if app.frequencybasedCheckBox.Value
                f.Message = append("Generating Clusters. Estimated processing time is ",string(estmdTime)," s");
            else
                f.Message = append("Generating Clusters... ");
            end
            %Create List of Folders to create Superclusters from
            Selected_Folders = unique([Selected_Measurements.Pfad]);

            for i = 1:length(Selected_Folders)
                Selected_Files = dir(append(Selected_Folders(i),"\4_Hüllkurven*\*.mat"));
                Selected_Paths = append(Selected_Files(1).folder,"\",Selected_Files(1).name);
                sData(i) = load(Selected_Paths);
            end

            Measurement_Names = [Selected_Measurements.Dateiname];

            [allTypes, allEnvs, allMems,allComps, nRowsMems, nRowsEnvs] = LoadDataforCluster(app,sData,Measurement_Names,app.min_freq,app.max_freq,app.freqres);

            %% frequency based clustering
            if app.frequencybasedCheckBox.Value

                sLinkMtrx = CalculateDistandLinkage(app,allEnvs,app.hierachical_distMetric);

                if app.customClstrNumber % manual number of superclusters
                    x = 1 : length(sLinkMtrx);
                    nSCltr = length(sLinkMtrx) - x;

                    %plotten der Linkage-Kurve
                    cla(app.LinkagePlotAxes,"reset")
                    hold(app.LinkagePlotAxes,"on");
                    plot(app.LinkagePlotAxes,nSCltr,sLinkMtrx(:,3),'Color','k','LineWidth',1.5);
                    xline(app.LinkagePlotAxes,app.NumberOfSuperClusters,"r","LineWidth",5)
                    xlabel(app.LinkagePlotAxes,"Number of Clusters [-]","FontSize",30);
                    ylabel(app.LinkagePlotAxes,"Error in Clusters [-]","FontSize",30);
                    xlim(app.LinkagePlotAxes,[0 1000])
                 else %automated number of superclusters
                    app.NumberOfSuperClusters = numberOfSuperclusters(app,sLinkMtrx(:,3),5,app.freqClstr_threshold);
                end

                if app.method_freq == "hierachical"
                    [app.srtdMems, app.srtdEnvs] = ClusterAndSort(app,allTypes,allMems,allEnvs, nRowsMems, nRowsEnvs, app.NumberOfSuperClusters,sLinkMtrx);

                elseif app.method_freq == "kMeans"
                    [app.srtdMems, app.srtdEnvs, ~,~,~] = ClusterAndSort_kMeans(app,allTypes,allMems,allEnvs, nRowsMems, nRowsEnvs, app.NumberOfSuperClusters,app.kMeans_distMetric);
                end
                % super envelopes
                [app.sEnvs_freq,app.sMems_freq] = calculateSuperEnvelopes(app,app.srtdEnvs,app.srtdMems,app.NumberOfSuperClusters,app.superEnvMethod);
                clear app.srtdMems app.srtdEnvs
            end

            %% componentbased clustering
            if app.componentbasedCheckBox.Value
                [app.srtdEnvsC,app.srtdMemsC,app.srtdCompsC]  = ClusterComponents(app,allEnvs,allMems,allComps);
                numberOfSuperclustersC = app.srtdEnvsC(end,1);
                [app.sEnvsC,app.sMemsC] = calculateSuperEnvelopes(app,app.srtdEnvsC,app.srtdMemsC,numberOfSuperclustersC,app.superEnvMethod);
            end

            %% position based clustering
            if app.positionbasedCheckBox.Value
                if isempty(app.CoGfiles)
                    uialert(app.DataAnalysisToolUIFigure,["No CoG data found!","positionbased clustering aborted!"],"Error","Icon","error")
                else

                    %boolean Vector, der angibt ob für Messung in der Datenbank
                    %CoG-Daten verfügbar sind
                    CoGdata_aval = contains([app.Measurement_Database.Baureihe],[app.CoGfiles.Baureihe]);

                    % Nachricht ausgeben, wenn keine CoG-Daten für die Auswahl
                    % gefunden wurden
                    CoG_data_Mask = and(CoGdata_aval,Selection_Mask);
                    fprintf(append("Found ",string(sum(CoG_data_Mask))," Measurements for CoG based Clustering",newline))
                    if ~any(CoG_data_Mask)
                        uialert(app.DataAnalysisToolUIFigure,["No CoG-Data for selected Measurements found!","Aborting Clustering by CoG-Position"],"Warning","Icon","warning")
                        app.CoGCluster_valid = false;
                    else
                        app.CoGCluster_valid = true;
                        %Ausgewählte Messungen für Clustern nach CoG-Position
                        Selected_Measurements_CoG = app.Measurement_Database(CoG_data_Mask);
                        %Create List of Folders to create Superclusters for
                        %position based Clustering
                        Selected_Folders = unique([Selected_Measurements_CoG.Pfad]);
                        for i = 1:length(Selected_Folders)
                            Selected_Files_CoG = dir(append(Selected_Folders(i),"\4_Hüllkurven*\*.mat"));
                            Selected_Paths_CoG = append(Selected_Files_CoG(1).folder,"\",Selected_Files_CoG(1).name);
                            sData_CoG(i) = load(Selected_Paths_CoG);
                        end
                        % Laden aller Daten, die Ausgewählt wurden und für
                        % die CoG Dateien vorhanden sind
                        Measurement_Names_CoG = [Selected_Measurements_CoG.Dateiname];
                        [~, allEnvs_CoG, allMems_CoG,allComps_CoG, ~, ~] = ...
                            LoadDataforCluster(app,sData_CoG,Measurement_Names_CoG,app.min_freq,app.max_freq,app.freqres);

                        %Aufrufen der Funktion zum Clustern nach
                        %CoG-Position
                        [app.srtdEnvsCoG,app.srtdMemsCoG] = ClusterCoGbased(app,allEnvs_CoG,allMems_CoG,allComps_CoG);

                        [app.sEnvsCoG,app.sMemsCoG] = calculateSuperEnvelopes(app,app.srtdEnvsCoG,app.srtdMemsCoG,app.NCoGClusters,app.superEnvMethod);

                    end
                end
            end

            f.Value = .9; f.Message = "Updating Measurements for Comparison...";
            updateComparisonFiles(app,Selection_Mask);
            app.spectr_outdated = false; %save that clusters are up to date to selected freq range

            f.Value = 1; f.Message = "Finished";
            close(f);

        end

        % Button pushed function: CompareDataButton
        function CompareDataButtonPushed(app, event)

            if isempty(app.sMems_freq) && isempty(app.sMemsC) && isempty(app.sMemsCoG)
                uialert(app.DataAnalysisToolUIFigure,append("No clusterdata for plotting found.",newline,"Please first run LvL 2 Clustering")...
                    ,"Error while plotting","Icon","warning");
                return;
            end

            %% reset vars and fields
            cla(app.Axes_Predicted_Envelopes,'reset')
            cla(app.componentbasedClustersAxes,'reset')
            cla(app.freqClustersAxes,'reset')
            cla(app.positionbasedClustersAxes,'reset')

            % Show Overview Plot
            app.Axes_Predicted_Envelopes.Visible = "on";
            hold(app.Axes_Predicted_Envelopes, 'on')

            % hide all axes of individual cluster methods
            app.componentbasedClustersAxes.Visible = "off";
            app.freqClustersAxes.Visible = "off";
            app.positionbasedClustersAxes.Visible = "off";

            % reset error text fields
            [app.MagnitudeerrorTextArea.Value, app.ShapeerrorTextArea.Value] = deal("","");
            [app.componentbased_Mag.Value, app.componentbased_Shape.Value] = deal("","");
            [app.positionbased_Mag.Value, app.positionbased_Shape.Value] = deal("","");

            app.pE_freq = 0;

            %% get values for further processing
            component = lower(app.SelectComponentEditField.Value);

            freqs = app.min_freq:app.freqres:app.max_freq;
            if app.spectr_outdated
                uialert(app.DataAnalysisToolUIFigure,["Frequency range in clusters is not up to date","Please recluster!"],"Warning","Icon","warning");
                return
            end
            y = ones(length(freqs),1);

            %selecting var to plot from
            if ~isempty(app.sMems_freq)
                Mems = app.sMems_freq;
                Envs = app.sEnvs_freq;
            elseif ~isempty(app.sMemsC)
                Mems = app.sMemsC;
                Envs = app.sEnvsC;
            else
                Mems = app.sMemsCoG;
                Envs = app.sEnvsCoG;
            end


            %% plot Envelope of freq. based Clustering
            if app.frequencybasedCheckBox.Value && ~isempty(app.sMems_freq)
                [app.pE_freq,componentInsEnvs,CoV_freq] = generatePredictionEnvelope(app,app.sEnvs_freq,app.sMems_freq,component,app.predictMthd);
                if any(componentInsEnvs)
                    app.selectedEnvs_freq = app.sEnvs_freq(find(componentInsEnvs),:);
                    [app.selectedMems_freq,app.selectedComp_freq] = convertMembers(app,app.sMems_freq,componentInsEnvs);
                    plot3(app.Axes_Predicted_Envelopes,freqs, y, app.pE_freq,'Color',[1 0 0 0.6], 'LineWidth', 2.5,...
                        "DisplayName",append("freq. based Prediction (mean std. dev.: ",string(CoV_freq)," m/s^2)"));
                    zlim(app.Axes_Predicted_Envelopes,[0 1.2*max(app.pE_freq)]);

                    %plot Clusters in freq based Clusters figure
                    plotClusters(app,app.freqClustersAxes,freqs,app.selectedEnvs_freq,app.pE_freq,[1 0 0 0.6])
                end
            end

            %% plot Envelope of Component based clustering
            if ~isempty(app.sMemsC) && app.componentbasedCheckBox.Value
                [app.pE_C,componentInsEnvs,CoV_comp] = generatePredictionEnvelope(app,app.sEnvsC,app.sMemsC,component,app.predictMthd);
                if any(componentInsEnvs)
                    app.selectedEnvs_Comp = app.sEnvsC(find(componentInsEnvs),:);
                    [app.selectedMems_Comp,app.selectedComp_Comp] = convertMembers(app,app.sMemsC,componentInsEnvs);
                    plotComp = plot3(app.Axes_Predicted_Envelopes,freqs, y, app.pE_C,...
                        'Color','#7E2F8E', 'LineWidth', 4, "DisplayName",append('component based Prediction (mean std. dev.: ',string(CoV_comp)," m/s^2)"));
                    plotComp.Color(4) = 0.6;
                    if max(app.pE_freq) < max(app.pE_C)
                        zlim(app.Axes_Predicted_Envelopes,[0 1.2*max(app.pE_C)]);
                    end

                    %plot Clusters in component based Clusters figure
                    plotClusters(app,app.componentbasedClustersAxes,freqs,app.selectedEnvs_Comp,app.pE_C,'#7E2F8E')
                end
            end

            %% plot Envelope of CoG based Clustering
            if ~isempty(app.sMemsCoG) && app.positionbasedCheckBox.Value
                [app.pE_CoG,componentInsEnvs,CoV_CoG] = generatePredictionEnvelope(app,app.sEnvsCoG,app.sMemsCoG,component,app.predictMthd);
                if any(componentInsEnvs)
                    app.selectedEnvs_CoG = app.sEnvsCoG(find(componentInsEnvs),:);
                    [app.selectedMems_CoG , app.selectedComp_CoG] = convertMembers(app,app.sMemsCoG,componentInsEnvs);
                    plotCoG = plot3(app.Axes_Predicted_Envelopes,freqs, y, app.pE_CoG,...
                        'Color','#EDB120', 'LineWidth', 2.5, "DisplayName",append('position based Prediction (mean std. dev.: ',string(CoV_CoG)," m/s^2)"));
                    plotCoG.Color(4) = 0.6;
                    if max(app.pE_freq) < max(app.pE_CoG)
                        zlim(app.Axes_Predicted_Envelopes,[0 1.2*max(app.pE_CoG)]);
                    end

                    %plot Clusters in position based Clusters figure
                    plotClusters(app,app.positionbasedClustersAxes,freqs,app.selectedEnvs_CoG,app.pE_CoG,'#EDB120')
                end
            end

            %% raise error when component couldn't be found in any envelopes
            if ~exist("componentInsEnvs","var") || ~any(componentInsEnvs)
                uialert(app.DataAnalysisToolUIFigure,"Component Input couldn't be matched to any existing component!","Error","Icon","error");
            end

            %% plot 2021 component when not predicting
            if ~isempty(app.MeasurementFileforComparisonDropDown.Items)

                if app.ShowComparisonCheckBox.Value
                    %--- Plot selected Comparison Measurement ---
                    Measurement_File_ID   = app.MeasurementFileforComparisonDropDown.Value; % get ID of Measurementfile entry in the database from DropDown (type: double)
                    Measurement_File_data = app.Measurement_Database(Measurement_File_ID); %get entry in Database for Measurement file based on ID (type: struct)
                    cPath = append(Measurement_File_data.Pfad,"\",Measurement_File_data.Unterpfad,"\",Measurement_File_data.Dateiname); %compose path to .txt file from database entry (type: string)
                    p = load(cPath); %load data of selected measurement file
                    plot3(app.Axes_Predicted_Envelopes,freqs, 3*y, p(app.loIndex:app.loIndex+app.fSteps,2), 'Color', 'b', 'LineWidth', 2.5,...
                        "DisplayName","Selected Comparison Measurement");
                end
                %--- plot Envelope of all ComparisonFiles ---
                Comparison_Files = app.Measurement_Database(app.MeasurementFileforComparisonDropDown.ItemsData);
                Comparison_Folders = unique([Comparison_Files.Pfad]);

                for i = 1:length(Comparison_Folders)
                    Selected_Files = dir(append(Comparison_Folders(i),"\4_Hüllkurven*\*.mat"));
                    Selected_Paths = append(Selected_Files(1).folder,"\",Selected_Files(1).name);
                    sData(i) = load(Selected_Paths);
                end

                [~, ComparisonEnvs, ComparisonMems,~, ~, ~] = ...
                    LoadDataforCluster(app,sData,app.MeasurementFileforComparisonDropDown.Items,app.min_freq,app.max_freq,app.freqres);
                ComparisonMems(:,4) = cellfun(@string,ComparisonMems(:,4),'UniformOutput',0);
                [app.pE_Comparison,~,CoV_compare] = generatePredictionEnvelope(app,ComparisonEnvs(:,4:end),ComparisonMems(:,4),component,'Maximum');
                plot3(app.Axes_Predicted_Envelopes,freqs, 3*y, app.pE_Comparison,...
                    'Color', 'k', 'LineWidth', 2.5,"DisplayName",append("Envelope of Comparison Measurements (mean std. dev.: ",string(CoV_compare)," m/s^2)"));
                if max([max(app.pE_freq),max(app.pE_CoG),max(app.pE_C)]) < max(app.pE_Comparison)
                    zlim(app.Axes_Predicted_Envelopes,[0 1.2*max(app.pE_Comparison)]);
                end
            end

            %% legend, labels, grid and view for prediction/comparison plot
            lgd = legend(app.Axes_Predicted_Envelopes,'Interpreter','none');
            lgd.Location    = "northeast";
            xlabel(app.Axes_Predicted_Envelopes,'frequency [Hz]');
            ylabel(app.Axes_Predicted_Envelopes,'clusternumber');
            zlabel(app.Axes_Predicted_Envelopes,'acceleration [m/s^2]');
            grid(app.Axes_Predicted_Envelopes,"on");
            set(app.Axes_Predicted_Envelopes,"FontSize",20)
            title(app.Axes_Predicted_Envelopes,append("Cluster Envelopes for ",component),"Interpreter","none");
            view(app.Axes_Predicted_Envelopes,0,0);

            %% Generate CoG Plot with highlighted Components in same freq. Cluster
            if app.frequencybasedCheckBox.Value && app.positionbasedCheckBox.Value && app.CoGCluster_valid
                PlotCoGsFreqClstComparison(app,component);
            end

            %% --- calculate errors ---
            if ~isempty(app.MeasurementFileforComparisonDropDown.Items)
                app.PredictionResultsPanel.Visible = true;

                if app.frequencybasedCheckBox.Value %calculate errors for freq based Clustering
                    [app.MagnitudeerrorTextArea.Value,app.ShapeerrorTextArea.Value] = calculateErrors(app,app.pE_Comparison,app.pE_freq);
                end

                if app.componentbasedCheckBox.Value %calculate error for component based clustering
                    [app.componentbased_Mag.Value,app.componentbased_Shape.Value] = calculateErrors(app,app.pE_Comparison,app.pE_C);
                end

                if app.positionbasedCheckBox.Value && app.CoGCluster_valid %calculate error for position based clustering
                    [app.positionbased_Mag.Value,app.positionbased_Shape.Value] = calculateErrors(app,app.pE_Comparison,app.pE_CoG);
                end
            else
                app.PredictionResultsPanel.Visible = false;
            end
        end

        % Value changed function: alternativeselectionmethodSwitch
        function alternativeselectionmethodSwitchValueChanged(app, event)
            value = app.alternativeselectionmethodSwitch.Value;
            if strcmpi(value,"Off")
                app.AltSelectionField.Editable = false;
                app.SelectedBuilstagesPanel.Enable = 'on';
                app.MeasurementSelection.Enable = true;
            elseif strcmpi(value,"On")
                app.AltSelectionField.Editable = true;
                app.SelectedBuilstagesPanel.Enable = 'off';
                app.MeasurementSelection.Enable = false;
            end
        end

        % Callback function: ReferenceYearDropDown,
        % ...and 2 other components
        function UpdateFilesforComparisonButtonPushed(app, event)
            Selection_Mask = getSelectionMask(app,false);
            updateComparisonFiles(app,Selection_Mask);
        end

        % Close request function: DataAnalysisToolUIFigure
        function DataAnalysisToolUIFigureCloseRequest(app, event)
            delete(app.SettingsAppHandle);
            delete(app);
        end

        % Menu selected function: SettingsMenu
        function SettingsMenuSelected(app, event)
            app.SettingsAppHandle = SettingsApp(app);
        end

        % Value changed function: frequencyrangeHzEditField
        function frequencyrangeHzEditFieldValueChanged(app, event)
            updateSelectedFrequencies(app);
        end

        % Value changed function: EditField
        function EditFieldValueChanged(app, event)
            updateSelectedFrequencies(app);
        end

        % Selection changed function: FunctionSelectionButtonGroup
        function FunctionSelectionButtonGroupSelectionChanged(app, event)
            if app.CompareButton.Value
                app.ComparetoyearLabel.Text = "Compare to year:";
                app.CompareDataButton.Text = "Compare Data";
            else
                app.ComparetoyearLabel.Text = "Year to predict:";
                app.CompareDataButton.Text = "Predict Envelope";
                app.realPrediction = true;
            end

        end

        % Selection changed function: EnvelopeGenerationMethodButtonGroup
        function EnvelopeGenerationMethodButtonGroupSelectionChanged(app, event)
            %selectedButton = app.EnvelopeGenerationMethodButtonGroup.SelectedObject;
            %app.predictMthd = selectedButton.Text;
        end

        % Menu selected function: PredictionPlotMenu
        function ExportPlot(app, event)
            newfigure = figure;
            ax1 = copyobj(app.Axes_Predicted_Envelopes,newfigure);
            ax1.Units = 'normalized';
            ax1.OuterPosition = [0 0 1 1];
            exportsetupdlg(newfigure);
        end

        % Menu selected function: ExcelxlsxMenu_2
        function ExportDatabaseToExcel(app, event)
            if isempty(app.Measurement_Database)
                uialert(app.DataAnalysisToolUIFigure,"No Database for Export found!","Export Database");
                return
            end
            writetable(struct2table(app.Measurement_Database),append(app.file_path,'\Measurement-Database.xlsx'),"Sheet","Measurment Database");
            uialert(app.DataAnalysisToolUIFigure,"Database Export successfull!","Export Database","Icon","success");
        end

        % Menu selected function: MatlabmatMenu_2
        function ExportDatabaseToMatlab(app, event)
            if isempty(app.Measurement_Database)
                uialert(app.DataAnalysisToolUIFigure,"No Database for Export found!","Export Database");
                return
            end
            Database = app.Measurement_Database;
            save(append(app.file_path,"\Measurement-Database.mat"),"Database");
            uialert(app.DataAnalysisToolUIFigure,"Database Export successfull!","Export Database","Icon","success");
        end

        % Menu selected function: ExcelxlsxMenu
        function ExportClusterdataToExcel(app, event)
            if isempty(app.selectedMems_Comp) && isempty(app.selectedMems_freq) && isempty(app.selectedMems_CoG)
                uialert(app.DataAnalysisToolUIFigure,"No data for Export found!","Error while Exporting Clusterdata");
                return
            end
            %write data from freq clustering to Excel
            if ~isempty(app.selectedMems_freq)
                exportDatatoExcel(app,app.selectedMems_freq,app.selectedEnvs_freq,...
                    app.selectedComp_freq,app.pE_freq,generateFilename(app,"Clusterdata_freqbased",".xlsx"));
            end
            %write data from Component based Clustering to Excel
            if ~isempty(app.selectedMems_Comp)
                exportDatatoExcel(app,app.selectedMems_Comp,app.selectedEnvs_Comp,...
                    app.selectedComp_Comp,app.pE_C,generateFilename(app,"Clusterdata_componentBased",".xlsx"));
            end

            %write data from pos based clustering to Excel
            if ~isempty(app.selectedMems_CoG)
                exportDatatoExcel(app,app.selectedMems_CoG,app.selectedEnvs_CoG,...
                    app.selectedComp_CoG,app.pE_CoG,generateFilename(app,"Clusterdata_positionbased",".xlsx"));
            end
            uialert(app.DataAnalysisToolUIFigure,"Clusterdata exported successfully!","Clusterdata Export","Icon","success");
        end

        % Menu selected function: MatlabmatMenu
        function ExportClusterdataToMatlab(app, event)
            if isempty(app.selectedMems_Comp) && isempty(app.selectedMems_freq) && isempty(app.selectedMems_CoG)
                uialert(app.DataAnalysisToolUIFigure,"No data for Export found!","Error while Exporting Clusterdata");
                return
            end
            %write data from freq based clustering to Matlab
            if ~isempty(app.selectedMems_freq)
                exportDataToMatlab(app,app.selectedMems_freq,app.selectedEnvs_freq,...
                    app.selectedComp_freq,app.pE_freq,generateFilename(app,"Clusterdata_freqbased",".mat"));
            end
            %write data from Component based Clustering to Matlab
            if ~isempty(app.selectedMems_Comp)
                exportDataToMatlab(app,app.selectedMems_Comp,app.selectedEnvs_Comp,...
                    app.selectedComp_Comp,app.pE_C,generateFilename(app,"Clusterdata_componentBased",".mat"));
            end

            %wirte data from position based Clustering to Matlab
            if ~isempty(app.selectedMems_CoG)
                exportDataToMatlab(app,app.selectedMems_CoG,app.selectedEnvs_CoG,...
                    app.selectedComp_CoG,app.pE_CoG,generateFilename(app,"Clusterdata_positionbased",".mat"));
            end

            uialert(app.DataAnalysisToolUIFigure,"Clusterdata exported successfully!","Clusterdata Export","Icon","success");
        end

        % Menu selected function: TranslationTableMenu
        function TranslationTableMenuSelected(app, event)
            cell_table = CoG_TranslationTable(app);
            Ncomps = size(cell_table,1);
            string_table = strings(Ncomps+2,1);

            string_table(1,1) = "Component Name in COG-Table";
            string_table(1,2) = "Component Names in measured freq. curves";

            string_table(3:end,1) = string(cell_table(:,1));

            for i = 1:Ncomps
                length_array = length(cell_table{i,2});
                for j = 1:length_array
                    string_table(i+2,j+1) = cell_table{i,2}(j);
                end
            end

            writematrix(string_table,append(app.file_path,"\TranslationTable.xlsx"))
            uialert(app.DataAnalysisToolUIFigure,"Translation Table exported successfully!","Translation Table Export","Icon","success");
        end

        % Value changed function: PredictionDropDown
        function PredictionDropDownValueChanged(app, event)
            app.predictMthd = app.PredictionDropDown.Value;
        end

        % Value changed function: ClusterDropDown
        function ClusterDropDownValueChanged(app, event)
            app.superEnvMethod = app.ClusterDropDown.Value;
        end
    end

    % Component initialization
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Get the file path for locating images
            pathToMLAPP = fileparts(mfilename('fullpath'));

            % Create DataAnalysisToolUIFigure and hide until all components are created
            app.DataAnalysisToolUIFigure = uifigure('Visible', 'off');
            app.DataAnalysisToolUIFigure.Position = [100 100 954 635];
            app.DataAnalysisToolUIFigure.Name = 'Data Analysis Tool';
            app.DataAnalysisToolUIFigure.Icon = fullfile(pathToMLAPP, 'Icon.png');
            app.DataAnalysisToolUIFigure.CloseRequestFcn = createCallbackFcn(app, @DataAnalysisToolUIFigureCloseRequest, true);

            % Create Menu
            app.Menu = uimenu(app.DataAnalysisToolUIFigure);
            app.Menu.Text = 'Menu';

            % Create ExportMenu
            app.ExportMenu = uimenu(app.Menu);
            app.ExportMenu.Text = 'Export...';

            % Create PredictionPlotMenu
            app.PredictionPlotMenu = uimenu(app.ExportMenu);
            app.PredictionPlotMenu.MenuSelectedFcn = createCallbackFcn(app, @ExportPlot, true);
            app.PredictionPlotMenu.Text = 'Prediction Plot';

            % Create DataofClustersMenu
            app.DataofClustersMenu = uimenu(app.ExportMenu);
            app.DataofClustersMenu.Text = 'Data of Clusters';

            % Create ExcelxlsxMenu
            app.ExcelxlsxMenu = uimenu(app.DataofClustersMenu);
            app.ExcelxlsxMenu.MenuSelectedFcn = createCallbackFcn(app, @ExportClusterdataToExcel, true);
            app.ExcelxlsxMenu.Text = 'Excel (.xlsx)';

            % Create MatlabmatMenu
            app.MatlabmatMenu = uimenu(app.DataofClustersMenu);
            app.MatlabmatMenu.MenuSelectedFcn = createCallbackFcn(app, @ExportClusterdataToMatlab, true);
            app.MatlabmatMenu.Text = 'Matlab (.mat)';

            % Create MeasurementDatabaseMenu
            app.MeasurementDatabaseMenu = uimenu(app.ExportMenu);
            app.MeasurementDatabaseMenu.Text = 'Measurement Database';

            % Create ExcelxlsxMenu_2
            app.ExcelxlsxMenu_2 = uimenu(app.MeasurementDatabaseMenu);
            app.ExcelxlsxMenu_2.MenuSelectedFcn = createCallbackFcn(app, @ExportDatabaseToExcel, true);
            app.ExcelxlsxMenu_2.Text = 'Excel (.xlsx)';

            % Create MatlabmatMenu_2
            app.MatlabmatMenu_2 = uimenu(app.MeasurementDatabaseMenu);
            app.MatlabmatMenu_2.MenuSelectedFcn = createCallbackFcn(app, @ExportDatabaseToMatlab, true);
            app.MatlabmatMenu_2.Text = 'Matlab (.mat)';

            % Create TranslationTableMenu
            app.TranslationTableMenu = uimenu(app.ExportMenu);
            app.TranslationTableMenu.MenuSelectedFcn = createCallbackFcn(app, @TranslationTableMenuSelected, true);
            app.TranslationTableMenu.Text = 'Translation Table';

            % Create SettingsMenu
            app.SettingsMenu = uimenu(app.Menu);
            app.SettingsMenu.MenuSelectedFcn = createCallbackFcn(app, @SettingsMenuSelected, true);
            app.SettingsMenu.Text = 'Settings...';

            % Create GridLayout
            app.GridLayout = uigridlayout(app.DataAnalysisToolUIFigure);
            app.GridLayout.ColumnWidth = {80, 60, 70, '1x', 40, 40, 40, 40, 40, 40, '1x', 40, 50, 40, 40, 50};
            app.GridLayout.RowHeight = {30, 30, 20, 25, 28, 30, 30, 30, 25, 30, 25, 30, 35, 15, 70, 25, 20, 20, 25, 50, '0.1x'};
            app.GridLayout.ColumnSpacing = 4.3;
            app.GridLayout.RowSpacing = 1.57894736842105;
            app.GridLayout.Padding = [4.26315789473684 1.57894736842105 4.26315789473684 1.57894736842105];

            % Create EnvelopeGenerationMethodButtonGroup
            app.EnvelopeGenerationMethodButtonGroup = uibuttongroup(app.GridLayout);
            app.EnvelopeGenerationMethodButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @EnvelopeGenerationMethodButtonGroupSelectionChanged, true);
            app.EnvelopeGenerationMethodButtonGroup.TitlePosition = 'centertop';
            app.EnvelopeGenerationMethodButtonGroup.Title = 'Envelope Generation Method:';
            app.EnvelopeGenerationMethodButtonGroup.Layout.Row = [12 14];
            app.EnvelopeGenerationMethodButtonGroup.Layout.Column = [13 16];

            % Create ClusterDropDownLabel
            app.ClusterDropDownLabel = uilabel(app.EnvelopeGenerationMethodButtonGroup);
            app.ClusterDropDownLabel.HorizontalAlignment = 'right';
            app.ClusterDropDownLabel.Position = [4 38 44 22];
            app.ClusterDropDownLabel.Text = 'Cluster';

            % Create ClusterDropDown
            app.ClusterDropDown = uidropdown(app.EnvelopeGenerationMethodButtonGroup);
            app.ClusterDropDown.Items = {'Maximum', 'Minimum', '+3*std.dev.(99%)', '+2*std.dev.(95%)', '+1*std.dev.(68%)', 'Mean', '99th-percentile (each freq.)', '95th-percentile (each freq.)', '75th-percentile (each freq.)', 'Median (each freq.)', '99th-percentile (total)', '95th-percentile (total)', '75th-percentile (total)', 'Median (total)'};
            app.ClusterDropDown.ValueChangedFcn = createCallbackFcn(app, @ClusterDropDownValueChanged, true);
            app.ClusterDropDown.Position = [68 38 122 22];
            app.ClusterDropDown.Value = 'Maximum';

            % Create PredictionDropDownLabel
            app.PredictionDropDownLabel = uilabel(app.EnvelopeGenerationMethodButtonGroup);
            app.PredictionDropDownLabel.HorizontalAlignment = 'right';
            app.PredictionDropDownLabel.Position = [4 9 59 22];
            app.PredictionDropDownLabel.Text = 'Prediction';

            % Create PredictionDropDown
            app.PredictionDropDown = uidropdown(app.EnvelopeGenerationMethodButtonGroup);
            app.PredictionDropDown.Items = {'Maximum', 'Minimum', '+3*std.dev.(99%)', '+2*std.dev.(95%)', '+1*std.dev.(68%)', 'Mean', '99th-percentile (each freq.)', '95th-percentile (each freq.)', '75th-percentile (each freq.)', 'Median (each freq.)', '99th-percentile (total)', '95th-percentile (total)', '75th-percentile (total)', 'Median (total)'};
            app.PredictionDropDown.ValueChangedFcn = createCallbackFcn(app, @PredictionDropDownValueChanged, true);
            app.PredictionDropDown.Position = [68 9 122 22];
            app.PredictionDropDown.Value = 'Maximum';

            % Create MeasurementSelection
            app.MeasurementSelection = uitree(app.GridLayout, 'checkbox');
            app.MeasurementSelection.Layout.Row = [1 21];
            app.MeasurementSelection.Layout.Column = [1 2];

            % Create AltSelectionField
            app.AltSelectionField = uieditfield(app.GridLayout, 'text');
            app.AltSelectionField.Editable = 'off';
            app.AltSelectionField.HorizontalAlignment = 'right';
            app.AltSelectionField.Layout.Row = 6;
            app.AltSelectionField.Layout.Column = [3 10];
            app.AltSelectionField.Value = 'K66;K67_BS0_FB_SERIE';

            % Create CompareDataButton
            app.CompareDataButton = uibutton(app.GridLayout, 'push');
            app.CompareDataButton.ButtonPushedFcn = createCallbackFcn(app, @CompareDataButtonPushed, true);
            app.CompareDataButton.BackgroundColor = [1 1 1];
            app.CompareDataButton.FontSize = 14;
            app.CompareDataButton.FontWeight = 'bold';
            app.CompareDataButton.Layout.Row = 10;
            app.CompareDataButton.Layout.Column = [13 16];
            app.CompareDataButton.Text = 'Compare Data';

            % Create ReferenceYearDropDown
            app.ReferenceYearDropDown = uidropdown(app.GridLayout);
            app.ReferenceYearDropDown.Items = {'2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2022', '2023'};
            app.ReferenceYearDropDown.ValueChangedFcn = createCallbackFcn(app, @UpdateFilesforComparisonButtonPushed, true);
            app.ReferenceYearDropDown.Layout.Row = 5;
            app.ReferenceYearDropDown.Layout.Column = [15 16];
            app.ReferenceYearDropDown.Value = '2021';

            % Create SetupButton
            app.SetupButton = uibutton(app.GridLayout, 'push');
            app.SetupButton.ButtonPushedFcn = createCallbackFcn(app, @SetupButtonPushed, true);
            app.SetupButton.BackgroundColor = [1 1 1];
            app.SetupButton.FontSize = 14;
            app.SetupButton.FontWeight = 'bold';
            app.SetupButton.Layout.Row = 1;
            app.SetupButton.Layout.Column = [13 16];
            app.SetupButton.Text = 'Setup';

            % Create MeasurementFileforComparisonDropDown
            app.MeasurementFileforComparisonDropDown = uidropdown(app.GridLayout);
            app.MeasurementFileforComparisonDropDown.Items = {};
            app.MeasurementFileforComparisonDropDown.Layout.Row = 9;
            app.MeasurementFileforComparisonDropDown.Layout.Column = [3 9];
            app.MeasurementFileforComparisonDropDown.Value = {};

            % Create MeasurementFileforComparisonDropDownLabel
            app.MeasurementFileforComparisonDropDownLabel = uilabel(app.GridLayout);
            app.MeasurementFileforComparisonDropDownLabel.Layout.Row = 8;
            app.MeasurementFileforComparisonDropDownLabel.Layout.Column = [3 6];
            app.MeasurementFileforComparisonDropDownLabel.Text = 'Measurement File for Comparison:';

            % Create ComparetoyearLabel
            app.ComparetoyearLabel = uilabel(app.GridLayout);
            app.ComparetoyearLabel.HorizontalAlignment = 'right';
            app.ComparetoyearLabel.Layout.Row = 5;
            app.ComparetoyearLabel.Layout.Column = [13 14];
            app.ComparetoyearLabel.Text = 'Compare to year:';

            % Create DataPreparationButton
            app.DataPreparationButton = uibutton(app.GridLayout, 'push');
            app.DataPreparationButton.ButtonPushedFcn = createCallbackFcn(app, @ButtonDataPreparationPushed, true);
            app.DataPreparationButton.BackgroundColor = [1 1 1];
            app.DataPreparationButton.FontSize = 14;
            app.DataPreparationButton.FontWeight = 'bold';
            app.DataPreparationButton.Layout.Row = 2;
            app.DataPreparationButton.Layout.Column = [13 16];
            app.DataPreparationButton.Text = 'DataPreparation';

            % Create SelectedBuilstagesPanel
            app.SelectedBuilstagesPanel = uipanel(app.GridLayout);
            app.SelectedBuilstagesPanel.TitlePosition = 'centertop';
            app.SelectedBuilstagesPanel.Title = 'Selected Builstages:';
            app.SelectedBuilstagesPanel.BackgroundColor = [0.9412 0.9412 0.9412];
            app.SelectedBuilstagesPanel.Layout.Row = [2 4];
            app.SelectedBuilstagesPanel.Layout.Column = [3 7];

            % Create BS1CheckBox
            app.BS1CheckBox = uicheckbox(app.SelectedBuilstagesPanel);
            app.BS1CheckBox.Text = 'BS1';
            app.BS1CheckBox.Position = [1 14 45 22];
            app.BS1CheckBox.Value = true;

            % Create BS0CheckBox
            app.BS0CheckBox = uicheckbox(app.SelectedBuilstagesPanel);
            app.BS0CheckBox.Text = 'BS0';
            app.BS0CheckBox.Position = [1 36 45 22];
            app.BS0CheckBox.Value = true;

            % Create ASCheckBox
            app.ASCheckBox = uicheckbox(app.SelectedBuilstagesPanel);
            app.ASCheckBox.Text = 'AS';
            app.ASCheckBox.Position = [134 35 38 22];
            app.ASCheckBox.Value = true;

            % Create VS2CheckBox
            app.VS2CheckBox = uicheckbox(app.SelectedBuilstagesPanel);
            app.VS2CheckBox.Text = 'VS2';
            app.VS2CheckBox.Position = [45 14 45 22];
            app.VS2CheckBox.Value = true;

            % Create VS1CheckBox
            app.VS1CheckBox = uicheckbox(app.SelectedBuilstagesPanel);
            app.VS1CheckBox.Text = 'VS1';
            app.VS1CheckBox.Position = [45 36 45 22];
            app.VS1CheckBox.Value = true;

            % Create SERIECheckBox
            app.SERIECheckBox = uicheckbox(app.SelectedBuilstagesPanel);
            app.SERIECheckBox.Text = 'SERIE';
            app.SERIECheckBox.Position = [134 14 58 22];
            app.SERIECheckBox.Value = true;

            % Create FBCheckBox
            app.FBCheckBox = uicheckbox(app.SelectedBuilstagesPanel);
            app.FBCheckBox.Text = 'FB';
            app.FBCheckBox.Position = [89 35 37 22];
            app.FBCheckBox.Value = true;

            % Create KEXCheckBox
            app.KEXCheckBox = uicheckbox(app.SelectedBuilstagesPanel);
            app.KEXCheckBox.Text = 'KEX';
            app.KEXCheckBox.Position = [89 14 46 22];
            app.KEXCheckBox.Value = true;

            % Create NotfoundCheckBox
            app.NotfoundCheckBox = uicheckbox(app.SelectedBuilstagesPanel);
            app.NotfoundCheckBox.Text = 'Not found';
            app.NotfoundCheckBox.Position = [176 37 74 22];
            app.NotfoundCheckBox.Value = true;

            % Create SelectedDirectionsPanel
            app.SelectedDirectionsPanel = uipanel(app.GridLayout);
            app.SelectedDirectionsPanel.TitlePosition = 'centertop';
            app.SelectedDirectionsPanel.Title = 'Selected Directions:';
            app.SelectedDirectionsPanel.BackgroundColor = [0.9412 0.9412 0.9412];
            app.SelectedDirectionsPanel.Layout.Row = [2 4];
            app.SelectedDirectionsPanel.Layout.Column = [8 10];

            % Create XCheckBox
            app.XCheckBox = uicheckbox(app.SelectedDirectionsPanel);
            app.XCheckBox.Text = '-X';
            app.XCheckBox.WordWrap = 'on';
            app.XCheckBox.Position = [1 35 34 22];
            app.XCheckBox.Value = true;

            % Create XCheckBox_2
            app.XCheckBox_2 = uicheckbox(app.SelectedDirectionsPanel);
            app.XCheckBox_2.Text = '+X';
            app.XCheckBox_2.Position = [1 19 37 22];
            app.XCheckBox_2.Value = true;

            % Create YCheckBox
            app.YCheckBox = uicheckbox(app.SelectedDirectionsPanel);
            app.YCheckBox.Text = '-Y';
            app.YCheckBox.Position = [37 35 34 22];
            app.YCheckBox.Value = true;

            % Create YCheckBox_2
            app.YCheckBox_2 = uicheckbox(app.SelectedDirectionsPanel);
            app.YCheckBox_2.Text = '+Y';
            app.YCheckBox_2.Position = [37 19 37 22];
            app.YCheckBox_2.Value = true;

            % Create ZCheckBox
            app.ZCheckBox = uicheckbox(app.SelectedDirectionsPanel);
            app.ZCheckBox.Text = '-Z';
            app.ZCheckBox.Position = [74 36 33 22];
            app.ZCheckBox.Value = true;

            % Create ZCheckBox_2
            app.ZCheckBox_2 = uicheckbox(app.SelectedDirectionsPanel);
            app.ZCheckBox_2.Text = '+Z';
            app.ZCheckBox_2.Position = [74 19 36 22];
            app.ZCheckBox_2.Value = true;

            % Create SelectComponentEditField
            app.SelectComponentEditField = uieditfield(app.GridLayout, 'text');
            app.SelectComponentEditField.ValueChangedFcn = createCallbackFcn(app, @UpdateFilesforComparisonButtonPushed, true);
            app.SelectComponentEditField.HorizontalAlignment = 'center';
            app.SelectComponentEditField.Layout.Row = 11;
            app.SelectComponentEditField.Layout.Column = [15 16];
            app.SelectComponentEditField.Value = 'Steuerkopf';

            % Create ComponentLabel
            app.ComponentLabel = uilabel(app.GridLayout);
            app.ComponentLabel.Layout.Row = 11;
            app.ComponentLabel.Layout.Column = [13 14];
            app.ComponentLabel.Text = 'Component:';

            % Create UpdateFilesforComparisonButton
            app.UpdateFilesforComparisonButton = uibutton(app.GridLayout, 'push');
            app.UpdateFilesforComparisonButton.ButtonPushedFcn = createCallbackFcn(app, @UpdateFilesforComparisonButtonPushed, true);
            app.UpdateFilesforComparisonButton.BackgroundColor = [1 1 1];
            app.UpdateFilesforComparisonButton.Layout.Row = 8;
            app.UpdateFilesforComparisonButton.Layout.Column = [6 9];
            app.UpdateFilesforComparisonButton.Text = 'Update Files for Comparison';

            % Create CustomNumberofSuperclustersPanel
            app.CustomNumberofSuperclustersPanel = uipanel(app.GridLayout);
            app.CustomNumberofSuperclustersPanel.Enable = 'off';
            app.CustomNumberofSuperclustersPanel.TitlePosition = 'centertop';
            app.CustomNumberofSuperclustersPanel.Title = 'Custom Number of Superclusters:';
            app.CustomNumberofSuperclustersPanel.Visible = 'off';
            app.CustomNumberofSuperclustersPanel.Layout.Row = [8 9];
            app.CustomNumberofSuperclustersPanel.Layout.Column = [13 16];
            app.CustomNumberofSuperclustersPanel.FontSize = 10;

            % Create NumberofSuperclustersEditField
            app.NumberofSuperclustersEditField = uieditfield(app.CustomNumberofSuperclustersPanel, 'text');
            app.NumberofSuperclustersEditField.HorizontalAlignment = 'center';
            app.NumberofSuperclustersEditField.Position = [29 7 148 22];
            app.NumberofSuperclustersEditField.Value = '30';

            % Create frequencyrangeHzEditFieldLabel
            app.frequencyrangeHzEditFieldLabel = uilabel(app.GridLayout);
            app.frequencyrangeHzEditFieldLabel.HorizontalAlignment = 'right';
            app.frequencyrangeHzEditFieldLabel.Layout.Row = 1;
            app.frequencyrangeHzEditFieldLabel.Layout.Column = [5 7];
            app.frequencyrangeHzEditFieldLabel.Text = 'frequency range [Hz]:';

            % Create frequencyrangeHzEditField
            app.frequencyrangeHzEditField = uieditfield(app.GridLayout, 'numeric');
            app.frequencyrangeHzEditField.Limits = [4 3200];
            app.frequencyrangeHzEditField.ValueChangedFcn = createCallbackFcn(app, @frequencyrangeHzEditFieldValueChanged, true);
            app.frequencyrangeHzEditField.HorizontalAlignment = 'center';
            app.frequencyrangeHzEditField.Layout.Row = 1;
            app.frequencyrangeHzEditField.Layout.Column = 8;
            app.frequencyrangeHzEditField.Value = 72;

            % Create EditFieldLabel
            app.EditFieldLabel = uilabel(app.GridLayout);
            app.EditFieldLabel.HorizontalAlignment = 'center';
            app.EditFieldLabel.FontWeight = 'bold';
            app.EditFieldLabel.Layout.Row = 1;
            app.EditFieldLabel.Layout.Column = 9;
            app.EditFieldLabel.Text = ' - ';

            % Create EditField
            app.EditField = uieditfield(app.GridLayout, 'numeric');
            app.EditField.Limits = [8 3200];
            app.EditField.ValueChangedFcn = createCallbackFcn(app, @EditFieldValueChanged, true);
            app.EditField.HorizontalAlignment = 'center';
            app.EditField.Layout.Row = 1;
            app.EditField.Layout.Column = 10;
            app.EditField.Value = 2000;

            % Create FunctionSelectionButtonGroup
            app.FunctionSelectionButtonGroup = uibuttongroup(app.GridLayout);
            app.FunctionSelectionButtonGroup.SelectionChangedFcn = createCallbackFcn(app, @FunctionSelectionButtonGroupSelectionChanged, true);
            app.FunctionSelectionButtonGroup.TitlePosition = 'centertop';
            app.FunctionSelectionButtonGroup.Title = 'Function Selection:';
            app.FunctionSelectionButtonGroup.Layout.Row = [6 7];
            app.FunctionSelectionButtonGroup.Layout.Column = [13 16];
            app.FunctionSelectionButtonGroup.FontWeight = 'bold';
            app.FunctionSelectionButtonGroup.FontSize = 14;

            % Create PredictButton
            app.PredictButton = uiradiobutton(app.FunctionSelectionButtonGroup);
            app.PredictButton.Text = 'Predict';
            app.PredictButton.FontSize = 14;
            app.PredictButton.Position = [29 8 66 22];

            % Create CompareButton
            app.CompareButton = uiradiobutton(app.FunctionSelectionButtonGroup);
            app.CompareButton.Text = 'Compare';
            app.CompareButton.FontSize = 14;
            app.CompareButton.Position = [111 8 79 22];
            app.CompareButton.Value = true;

            % Create alternativeselectionmethodSwitchLabel
            app.alternativeselectionmethodSwitchLabel = uilabel(app.GridLayout);
            app.alternativeselectionmethodSwitchLabel.HorizontalAlignment = 'right';
            app.alternativeselectionmethodSwitchLabel.Layout.Row = 5;
            app.alternativeselectionmethodSwitchLabel.Layout.Column = [3 7];
            app.alternativeselectionmethodSwitchLabel.Text = 'alternative selection method:';

            % Create alternativeselectionmethodSwitch
            app.alternativeselectionmethodSwitch = uiswitch(app.GridLayout, 'slider');
            app.alternativeselectionmethodSwitch.ValueChangedFcn = createCallbackFcn(app, @alternativeselectionmethodSwitchValueChanged, true);
            app.alternativeselectionmethodSwitch.FontSize = 10;
            app.alternativeselectionmethodSwitch.Layout.Row = 5;
            app.alternativeselectionmethodSwitch.Layout.Column = [8 10];

            % Create PredictionResultsPanel
            app.PredictionResultsPanel = uipanel(app.GridLayout);
            app.PredictionResultsPanel.TitlePosition = 'centertop';
            app.PredictionResultsPanel.Title = 'Prediction Results:';
            app.PredictionResultsPanel.Layout.Row = [15 20];
            app.PredictionResultsPanel.Layout.Column = [13 16];

            % Create freqbasedLabel
            app.freqbasedLabel = uilabel(app.PredictionResultsPanel);
            app.freqbasedLabel.VerticalAlignment = 'bottom';
            app.freqbasedLabel.Position = [2 138 134 16];
            app.freqbasedLabel.Text = 'freq. based';

            % Create MagnitudeerrorTextAreaLabel
            app.MagnitudeerrorTextAreaLabel = uilabel(app.PredictionResultsPanel);
            app.MagnitudeerrorTextAreaLabel.HorizontalAlignment = 'center';
            app.MagnitudeerrorTextAreaLabel.VerticalAlignment = 'top';
            app.MagnitudeerrorTextAreaLabel.FontWeight = 'bold';
            app.MagnitudeerrorTextAreaLabel.Position = [0 153 98 41];
            app.MagnitudeerrorTextAreaLabel.Text = {'Magnitude Error'; '[kHz*m/s^2]'};

            % Create MagnitudeerrorTextArea
            app.MagnitudeerrorTextArea = uitextarea(app.PredictionResultsPanel);
            app.MagnitudeerrorTextArea.Editable = 'off';
            app.MagnitudeerrorTextArea.HorizontalAlignment = 'center';
            app.MagnitudeerrorTextArea.Position = [2 114 85 20];

            % Create ShapeerrorTextArea
            app.ShapeerrorTextArea = uitextarea(app.PredictionResultsPanel);
            app.ShapeerrorTextArea.Editable = 'off';
            app.ShapeerrorTextArea.HorizontalAlignment = 'center';
            app.ShapeerrorTextArea.Position = [103 114 85 20];

            % Create ShapeerrorTextAreaLabel
            app.ShapeerrorTextAreaLabel = uilabel(app.PredictionResultsPanel);
            app.ShapeerrorTextAreaLabel.HorizontalAlignment = 'center';
            app.ShapeerrorTextAreaLabel.VerticalAlignment = 'top';
            app.ShapeerrorTextAreaLabel.FontWeight = 'bold';
            app.ShapeerrorTextAreaLabel.Position = [102 152 88 42];
            app.ShapeerrorTextAreaLabel.Text = {'Conformity '; 'of Shape'; '[ - ]'};

            % Create componentbasedEditFieldLabel
            app.componentbasedEditFieldLabel = uilabel(app.PredictionResultsPanel);
            app.componentbasedEditFieldLabel.VerticalAlignment = 'bottom';
            app.componentbasedEditFieldLabel.Position = [2 89 101 15];
            app.componentbasedEditFieldLabel.Text = 'component based';

            % Create componentbased_Mag
            app.componentbased_Mag = uieditfield(app.PredictionResultsPanel, 'text');
            app.componentbased_Mag.Editable = 'off';
            app.componentbased_Mag.HorizontalAlignment = 'center';
            app.componentbased_Mag.Position = [2 62 85 20];

            % Create componentbased_Shape
            app.componentbased_Shape = uieditfield(app.PredictionResultsPanel, 'text');
            app.componentbased_Shape.Editable = 'off';
            app.componentbased_Shape.HorizontalAlignment = 'center';
            app.componentbased_Shape.Position = [103 62 85 20];

            % Create positionbasedEditFieldLabel
            app.positionbasedEditFieldLabel = uilabel(app.PredictionResultsPanel);
            app.positionbasedEditFieldLabel.VerticalAlignment = 'bottom';
            app.positionbasedEditFieldLabel.Position = [2 40 83 15];
            app.positionbasedEditFieldLabel.Text = 'position based';

            % Create positionbased_Mag
            app.positionbased_Mag = uieditfield(app.PredictionResultsPanel, 'text');
            app.positionbased_Mag.Editable = 'off';
            app.positionbased_Mag.HorizontalAlignment = 'center';
            app.positionbased_Mag.Position = [2 13 85 20];

            % Create positionbased_Shape
            app.positionbased_Shape = uieditfield(app.PredictionResultsPanel, 'text');
            app.positionbased_Shape.Editable = 'off';
            app.positionbased_Shape.HorizontalAlignment = 'center';
            app.positionbased_Shape.Position = [103 13 85 20];

            % Create ClusterButton
            app.ClusterButton = uibutton(app.GridLayout, 'push');
            app.ClusterButton.ButtonPushedFcn = createCallbackFcn(app, @ClusterButtonPushed, true);
            app.ClusterButton.BackgroundColor = [1 1 1];
            app.ClusterButton.FontSize = 14;
            app.ClusterButton.FontWeight = 'bold';
            app.ClusterButton.Layout.Row = [3 4];
            app.ClusterButton.Layout.Column = [13 16];
            app.ClusterButton.Text = 'Cluster';

            % Create ClusteringMethodsPanel
            app.ClusteringMethodsPanel = uipanel(app.GridLayout);
            app.ClusteringMethodsPanel.TitlePosition = 'centertop';
            app.ClusteringMethodsPanel.Title = 'Clustering Methods:';
            app.ClusteringMethodsPanel.Layout.Row = [1 4];
            app.ClusteringMethodsPanel.Layout.Column = [11 12];
            app.ClusteringMethodsPanel.FontSize = 14;

            % Create frequencybasedCheckBox
            app.frequencybasedCheckBox = uicheckbox(app.ClusteringMethodsPanel);
            app.frequencybasedCheckBox.Text = 'frequency based';
            app.frequencybasedCheckBox.Position = [4 60 111 22];
            app.frequencybasedCheckBox.Value = true;

            % Create componentbasedCheckBox
            app.componentbasedCheckBox = uicheckbox(app.ClusteringMethodsPanel);
            app.componentbasedCheckBox.Text = 'component based';
            app.componentbasedCheckBox.Position = [4 39 118 22];
            app.componentbasedCheckBox.Value = true;

            % Create positionbasedCheckBox
            app.positionbasedCheckBox = uicheckbox(app.ClusteringMethodsPanel);
            app.positionbasedCheckBox.Text = 'position based';
            app.positionbasedCheckBox.Position = [4 19 118 22];
            app.positionbasedCheckBox.Value = true;

            % Create TabGroup
            app.TabGroup = uitabgroup(app.GridLayout);
            app.TabGroup.Layout.Row = [11 21];
            app.TabGroup.Layout.Column = [3 12];

            % Create OverviewTab
            app.OverviewTab = uitab(app.TabGroup);
            app.OverviewTab.Title = 'Overview';

            % Create Axes_Predicted_Envelopes
            app.Axes_Predicted_Envelopes = uiaxes(app.OverviewTab);
            app.Axes_Predicted_Envelopes.FontSize = 18;
            app.Axes_Predicted_Envelopes.Position = [1 2 572 309];

            % Create freqbasedClustersTab
            app.freqbasedClustersTab = uitab(app.TabGroup);
            app.freqbasedClustersTab.Title = 'freq. based Clusters';

            % Create freqClustersAxes
            app.freqClustersAxes = uiaxes(app.freqbasedClustersTab);
            xlabel(app.freqClustersAxes, 'X')
            ylabel(app.freqClustersAxes, 'acceleration [m/s^2]')
            zlabel(app.freqClustersAxes, 'Z')
            app.freqClustersAxes.FontSize = 20;
            app.freqClustersAxes.Visible = 'off';
            app.freqClustersAxes.Position = [1 1 571 310];

            % Create compbasedClustersTab
            app.compbasedClustersTab = uitab(app.TabGroup);
            app.compbasedClustersTab.Title = 'comp. based Clusters';

            % Create componentbasedClustersAxes
            app.componentbasedClustersAxes = uiaxes(app.compbasedClustersTab);
            title(app.componentbasedClustersAxes, 'component based Clusters')
            xlabel(app.componentbasedClustersAxes, 'X')
            ylabel(app.componentbasedClustersAxes, 'Y')
            zlabel(app.componentbasedClustersAxes, 'Z')
            app.componentbasedClustersAxes.Visible = 'off';
            app.componentbasedClustersAxes.Position = [1 5 573 305];

            % Create positionbasedClustersTab
            app.positionbasedClustersTab = uitab(app.TabGroup);
            app.positionbasedClustersTab.Title = 'position based Clusters';

            % Create positionbasedClustersAxes
            app.positionbasedClustersAxes = uiaxes(app.positionbasedClustersTab);
            title(app.positionbasedClustersAxes, 'position based Clusters')
            xlabel(app.positionbasedClustersAxes, 'X')
            ylabel(app.positionbasedClustersAxes, 'Y')
            zlabel(app.positionbasedClustersAxes, 'Z')
            app.positionbasedClustersAxes.Visible = 'off';
            app.positionbasedClustersAxes.Position = [1 1 571 310];

            % Create CoGPositionsTab
            app.CoGPositionsTab = uitab(app.TabGroup);
            app.CoGPositionsTab.Title = 'CoG Positions';

            % Create CoGPositionsAxes
            app.CoGPositionsAxes = uiaxes(app.CoGPositionsTab);
            title(app.CoGPositionsAxes, 'CoG Positions of Components')
            xlabel(app.CoGPositionsAxes, 'X [mm]')
            ylabel(app.CoGPositionsAxes, 'Y [mm]')
            zlabel(app.CoGPositionsAxes, 'Z')
            app.CoGPositionsAxes.Visible = 'off';
            app.CoGPositionsAxes.Position = [11 6 563 304];

            % Create LinkageTab
            app.LinkageTab = uitab(app.TabGroup);
            app.LinkageTab.Title = 'Linkage';

            % Create LinkagePlotAxes
            app.LinkagePlotAxes = uiaxes(app.LinkageTab);
            title(app.LinkagePlotAxes, 'Title')
            xlabel(app.LinkagePlotAxes, 'X')
            ylabel(app.LinkagePlotAxes, 'Y')
            zlabel(app.LinkagePlotAxes, 'Z')
            app.LinkagePlotAxes.Position = [2 2 564 307];

            % Create ShowComparisonCheckBox
            app.ShowComparisonCheckBox = uicheckbox(app.GridLayout);
            app.ShowComparisonCheckBox.Text = 'Show';
            app.ShowComparisonCheckBox.Layout.Row = 9;
            app.ShowComparisonCheckBox.Layout.Column = [10 11];
            app.ShowComparisonCheckBox.Value = true;

            % Show the figure after all components are created
            app.DataAnalysisToolUIFigure.Visible = 'on';
        end
    end

    % App creation and deletion
    methods (Access = public)

        % Construct app
        function app = DataAnalysisTool

            runningApp = getRunningApp(app);

            % Check for running singleton app
            if isempty(runningApp)

                % Create UIFigure and components
                createComponents(app)

                % Register the app with App Designer
                registerApp(app, app.DataAnalysisToolUIFigure)

                % Execute the startup function
                runStartupFcn(app, @startupFcn)
            else

                % Focus the running singleton app
                figure(runningApp.DataAnalysisToolUIFigure)

                app = runningApp;
            end

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.DataAnalysisToolUIFigure)
        end
    end
end