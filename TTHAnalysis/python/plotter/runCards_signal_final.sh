#!/bin/bash

#######################################################OTHER A BOSON masses#####################################################
	
python makeShapeCardsSusy.py mcaET_UW2.txt cuts_ET.txt A_svFit_constrained 30,0,600 systs_AZh.txt \
-P AZh_MC --skimPath \
--Fs sf/t massesMC_Sep07/{cname}.root \
--FMC sf/t scalesMC_July8/{cname}.root \
    --od /afs/cern.ch/work/j/jheikkil/testaus/CMSSW_9_4_6_patch1/src/HiggsAnalysis/CombinedLimit/cardsOS_final_0705/MMET/Aconstr_HsvFit90 -l 35.9 -A "entry point" zeromass2 "H_svFit_constrained > 0 && H_svFit>90 && H_svFit < 180 && A_svFit_constrained<600" \
-W 'weight_gen*puweight*electronSF_1*electronSF_2*electronSF_3*electronSF_4*muonSF_1*muonSF_2*muonSF_3*muonSF_4*tauSF_3*tauSF_4*zhTrigWeight*massSF' -j 6 --neg --xp "WZ"   --hardZero     -b MMET --xf .*EEET.* ;

python makeShapeCardsSusy.py mcaET_UW2.txt cuts_ET.txt A_svFit_constrained 30,0,600 systs_AZh.txt \
-P AZh_MC --skimPath \
--Fs sf/t massesMC_Sep07/{cname}.root \
--FMC sf/t scalesMC_July8/{cname}.root \
    --od /afs/cern.ch/work/j/jheikkil/testaus/CMSSW_9_4_6_patch1/src/HiggsAnalysis/CombinedLimit/cardsOS_final_0705/EEET/Aconstr_HsvFit90 -l 35.9 -A "entry point" zeromass2 "H_svFit_constrained > 0 && H_svFit>90 && H_svFit < 180 && A_svFit_constrained<600" \
-W 'weight_gen*puweight*electronSF_1*electronSF_2*electronSF_3*electronSF_4*muonSF_1*muonSF_2*muonSF_3*muonSF_4*tauSF_3*tauSF_4*zhTrigWeight*massSF' -j 6 --neg --xp "WZ"   --hardZero    -b EEET --xf .*MMET.* ;

python makeShapeCardsSusy.py mcaTT_UW2.txt cuts_TT.txt A_svFit_constrained 30,0,600 systs_AZh.txt \
-P AZh_MC --skimPath \
--Fs sf/t massesMC_Sep07/{cname}.root \
--FMC sf/t scalesMC_July8/{cname}.root \
    --od /afs/cern.ch/work/j/jheikkil/testaus/CMSSW_9_4_6_patch1/src/HiggsAnalysis/CombinedLimit/cardsOS_final_0705/EETT/Aconstr_HsvFit90 -l 35.9 -A "entry point" zeromass2 "H_svFit_constrained > 0 && H_svFit>90 && H_svFit < 180 && A_svFit_constrained<600" \
-W 'weight_gen*puweight*electronSF_1*electronSF_2*electronSF_3*electronSF_4*muonSF_1*muonSF_2*muonSF_3*muonSF_4*tauSF_3*tauSF_4*zhTrigWeight*massSF' -j 6 --neg --xp "WZ"   --hardZero    -b EETT --xf .*MMTT.* ;

python makeShapeCardsSusy.py mcaTT_UW2.txt cuts_TT.txt A_svFit_constrained 30,0,600 systs_AZh.txt \
-P AZh_MC --skimPath \
--Fs sf/t massesMC_Sep07/{cname}.root \
--FMC sf/t scalesMC_July8/{cname}.root \
    --od /afs/cern.ch/work/j/jheikkil/testaus/CMSSW_9_4_6_patch1/src/HiggsAnalysis/CombinedLimit/cardsOS_final_0705/MMTT/Aconstr_HsvFit90 -l 35.9 -A "entry point" zeromass2 "H_svFit_constrained > 0 && H_svFit>90 && H_svFit < 180 && A_svFit_constrained<600" \
-W 'weight_gen*puweight*electronSF_1*electronSF_2*electronSF_3*electronSF_4*muonSF_1*muonSF_2*muonSF_3*muonSF_4*tauSF_3*tauSF_4*zhTrigWeight*massSF' -j 6 --neg --xp "WZ"   --hardZero   -b MMTT --xf .*EETT.* ;

python makeShapeCardsSusy.py mcaMT_UW2.txt cuts_MT.txt A_svFit_constrained 30,0,600 systs_AZh.txt \
-P AZh_MC --skimPath \
--Fs sf/t massesMC_Sep07/{cname}.root \
--FMC sf/t scalesMC_July8/{cname}.root \
    --od /afs/cern.ch/work/j/jheikkil/testaus/CMSSW_9_4_6_patch1/src/HiggsAnalysis/CombinedLimit/cardsOS_final_0705/MMMT/Aconstr_HsvFit90 -l 35.9 -A "entry point" zeromass2 "H_svFit_constrained > 0 && H_svFit>90 && H_svFit < 180 && A_svFit_constrained<600" \
-W 'weight_gen*puweight*electronSF_1*electronSF_2*electronSF_3*electronSF_4*muonSF_1*muonSF_2*muonSF_3*muonSF_4*tauSF_3*tauSF_4*zhTrigWeight*massSF' -j 6 --neg --xp "WZ"   --hardZero    -b MMMT --xf .*EEMT.* ;

python makeShapeCardsSusy.py mcaMT_UW2.txt cuts_MT.txt A_svFit_constrained 30,0,600 systs_AZh.txt \
-P AZh_MC --skimPath \
--Fs sf/t massesMC_Sep07/{cname}.root \
--FMC sf/t scalesMC_July8/{cname}.root \
    --od /afs/cern.ch/work/j/jheikkil/testaus/CMSSW_9_4_6_patch1/src/HiggsAnalysis/CombinedLimit/cardsOS_final_0705/EEMT/Aconstr_HsvFit90 -l 35.9 -A "entry point" zeromass2 "H_svFit_constrained > 0 && H_svFit>90 && H_svFit < 180 && A_svFit_constrained<600" \
-W 'weight_gen*puweight*electronSF_1*electronSF_2*electronSF_3*electronSF_4*muonSF_1*muonSF_2*muonSF_3*muonSF_4*tauSF_3*tauSF_4*zhTrigWeight*massSF' -j 6 --neg --xp "WZ"   --hardZero    -b EEMT --xf .*MMMT.* ;

python makeShapeCardsSusy.py mcaEM_UW2.txt cuts_EM.txt A_svFit_constrained 30,0,600 systs_AZh.txt \
-P AZh_MC --skimPath \
--Fs sf/t massesMC_Sep07/{cname}.root \
--FMC sf/t scalesMC_July8/{cname}.root \
    --od /afs/cern.ch/work/j/jheikkil/testaus/CMSSW_9_4_6_patch1/src/HiggsAnalysis/CombinedLimit/cardsOS_final_0705/MMEM/Aconstr_HsvFit90 -l 35.9 -A "entry point" zeromass2 "H_svFit_constrained > 0 && H_svFit>90 && H_svFit < 180 && A_svFit_constrained<600" \
-W 'weight_gen*puweight*electronSF_1*electronSF_2*electronSF_3*electronSF_4*muonSF_1*muonSF_2*muonSF_3*muonSF_4*tauSF_3*tauSF_4*zhTrigWeight*massSF' -j 6 --neg --xp "WZ"   --hardZero    -b MMEM --xf .*EEEM.* ;

python makeShapeCardsSusy.py mcaEM_UW2.txt cuts_EM.txt A_svFit_constrained 30,0,600 systs_AZh.txt \
-P AZh_MC --skimPath \
--Fs sf/t massesMC_Sep07/{cname}.root \
--FMC sf/t scalesMC_July8/{cname}.root \
    --od /afs/cern.ch/work/j/jheikkil/testaus/CMSSW_9_4_6_patch1/src/HiggsAnalysis/CombinedLimit/cardsOS_final_0705/EEEM/Aconstr_HsvFit90 -l 35.9 -A "entry point" zeromass2 "H_svFit_constrained > 0 && H_svFit>90 && H_svFit < 180 && A_svFit_constrained<600" \
-W 'weight_gen*puweight*electronSF_1*electronSF_2*electronSF_3*electronSF_4*muonSF_1*muonSF_2*muonSF_3*muonSF_4*tauSF_3*tauSF_4*zhTrigWeight*massSF' -j 6 --neg --xp "WZ"   --hardZero    -b EEEM --xf .*MMEM.* ;