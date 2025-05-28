#ifdef __CLING__
gSystem->AddIncludePath("-I/$WORK/Delphes/");
R__LOAD_LIBRARY(libDelphes.so)
#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#include "external/fastjet/contribs/LundPlugin/LundWithSecondary.hh"
#include "external/fastjet/contribs/LundPlugin/LundJSON.hh"
#include "external/fastjet/PseudoJet.hh"
#include <cstdlib> // for integer abs
#include <cmath>   // for floating point abs
#endif


using namespace std;

void read_event(vector<fastjet::PseudoJet> &event, TClonesArray *branchParticle, TObject *object, GenParticle *particle, ofstream &outfile) {
    bool firstParticle = true;
    outfile << "      \"particles\": [" << endl;
    
    for (int i = 0; i < branchParticle->GetEntriesFast(); i++) {
        GenParticle *particle = (GenParticle*) branchParticle->At(i);
        if (!particle) continue;
        
        double particle_PID = particle->PID;
        double particle_Status = particle->Status;
        int pid = std::abs(particle_PID);
        
//        if (((pid / 100000 == 49) && ((pid % 1000) / 100 >= 1) && (pid % 10 == 3))) {
        if ((std::abs(particle_Status) == 1) &&
        //    (std::abs(particle_PID) != 22) &&
            (std::abs(particle_PID) != 4900111) &&  (std::abs(particle_PID) != 4900211) &&  ((std::abs(particle_PID)<= 4900102) || (std::abs(pid)%10 != 1)) && 
            (std::abs(particle_PID) != 12) && 
            (std::abs(particle_PID) != 14) && 
            (std::abs(particle_PID) != 16) && 
            (std::abs(particle_PID) != 51) && 
            (std::abs(particle_PID) != 53)) { 
            fastjet::PseudoJet pseudoJet(particle->P4().Px(), particle->P4().Py(), particle->P4().Pz(), particle->P4().E());
            pseudoJet.set_user_index(particle->PID);  // Store PID here

            event.push_back(pseudoJet);
            
            if (!firstParticle) outfile << ",\n";
            outfile << "         { \"particle_PID\": " << particle->PID
                    << ", \"Px\": " << particle->P4().Px()
                    << ", \"Py\": " << particle->P4().Py()
                    << ", \"Pz\": " << particle->P4().Pz()
                    << ", \"E\": " << particle->P4().E() 
                    << ", \"Status\":" << particle->Status << " }";
            firstParticle = false;
        }
    }
    outfile << "\n      ]," << endl;
}

void testing_json(const char* fileName, const char* Output_path) {
    gSystem->Load("libDelphes");
    TChain chain("Delphes");
    chain.Add(fileName);
    ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
    Long64_t numberOfEntries = treeReader->GetEntries();
    TClonesArray *branchParticle = treeReader->UseBranch("Particle");
    
    TObject *object;
    GenParticle *particle;
    
    stringstream ss;
    ss << Output_path << "/jets_Scan.json";
    string filename = ss.str();
    
    cout << "# Writing data to " << filename << endl;
    
    ofstream outfile;
    outfile.open(filename);
    outfile << "{\n  \"events\": [\n";
    double R = 0.8, ptmin = 200.0, ptmax = 1000.0;
    
    for(Int_t entry = 0; entry < (numberOfEntries < 40000L ? numberOfEntries : 40000L); ++entry) { 
        treeReader->ReadEntry(entry);
        outfile << "   {\n      \"event_index\": " << entry << ",\n";
        
        vector<fastjet::PseudoJet> event;
        read_event(event, branchParticle, object, particle, outfile);
        
        fastjet::JetDefinition jet_def(fastjet::antikt_algorithm, 0.8);
        fastjet::ClusterSequence cs(event, jet_def);
        vector<fastjet::PseudoJet> jets = sorted_by_pt(cs.inclusive_jets(ptmin));
        for(auto it = jets.begin(); it != jets.end();){
            if(it->perp() > ptmax){
                it = jets.erase(it);
            }else{
                ++it;
            }
        }
        cout  << "Number of clustered jets: " << jets.size() << endl;
        
        fastjet::contrib::SecondaryLund_mMDT secondary;
        fastjet::contrib::LundWithSecondary lund(&secondary);
        
        outfile << "      \"lund_declustering\": [\n";
        for (unsigned ijet = 0; ijet < jets.size(); ijet++) {
            vector<fastjet::contrib::LundDeclustering> declusts = lund.primary(jets[ijet]);
            outfile << "         { \"jet_index\": " << ijet << ", \"declusterings\": ";
            lund_to_json(outfile, declusts);
            outfile << " }";
            if (ijet < jets.size() - 1) outfile << ",\n";
        }
        outfile << "\n      ],\n";
        
        outfile << "      \"number_of_particles\": " << event.size() << "\n   }";
        
        if (entry < numberOfEntries - 1) outfile << ",\n"; 
    }
    
    outfile << "\n  ]\n}" << endl;
    outfile.close();
    cout << "# JSON output written successfully!" << endl;
}
