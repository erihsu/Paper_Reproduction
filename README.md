# Paper_Reproduction
reproduction paper researching in Ultra-low voltage (ULV) clock tree design

# DP+DME



DP+DME algorithm is proposed by Xin Zhao in 2010[1] to optimize clock tree slew and skew at ULV. The reproduction code is located in **DP_DME** folder.


# BufH

In [2], Seok proposed an un-buffered H-tree (or few clock buffer level) method to dramatically reduce clock skew variation at ULV. For impressive purpose , the buffered-Htree with limited buffer stage level is implemented in **H-Tree** folder. 





#### Reference

[[1]](https://drive.google.com/file/d/1EDHklBIlDvOlwln5HmBJMbFlZlWSy5vJ/view?usp=sharing)Zhao, Xin, et al. "Variation-aware clock network design methodology for ultralow voltage (ULV) circuits." *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems* 31.8 (2012): 1222-1234.

[[2]](https://drive.google.com/file/d/1IH5j_FlfenFgr2vIS6LNwAvcRrhCVRd6/view?usp=sharing)[Seok, Mingoo, David Blaauw, and Dennis Sylvester. "Robust clock network design methodology for ultra-low voltage operations." *IEEE Journal on Emerging and Selected Topics in Circuits and Systems* 1.2 (2011): 120-130.