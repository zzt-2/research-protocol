#!/usr/bin/env python3
"""
Apply 56 author updates from sub-agent web search results + 2 citekey renames.
"""

import re
from pathlib import Path

BIB_PATH = Path("毕设/写作材料/references.bib")
LIT_PATH = Path("毕设/写作材料/material-chapter-literature.md")

# Author updates: citekey -> full author string
AUTHORS = {
    # Batch A
    "almogahed2022": "Almogahed and Amphawan and Mohammed and Alawadhi",
    "czerwinski2025": "Czerwinski and Borkowski and Haddadi",
    "heine2015edrs": "Zech and Heine and Trondl and Seel and Motzigemba and Meyer and Philipp-May",
    "vaithianathan2024": "Vaithianathan and Udkar and Roy and Reddy and Rajasekaran",
    "zhou2022jlt": "Zhou and Zhang and Song and Hu and Song and Zou and Su and Zhao and Pang and Almaiman and Liu and Minoofar and Tur and Willner",
    "sun2020": "Sun and Huang and Yao and Guo",
    "zhang2018": "Zhang and Wang and Liu and Guo and Li and Wang",
    "mcdonald2025": "McDonald and Bellossi and Gladysz",
    "gong2015": "Gong and Xu",
    "tang2023fso": "Tang and Wang and Zhang and Cai and Li and Zhang",
    "li2021": "Li and Geng and Wu and Gao and Li",
    "barbosa2020": "Mello and Barbosa and Reis",
    "melo2018": "Mello and Barbosa and Reis",
    "rozental2017": "Rozental and Kong and Foo and Corcoran and Lowery",
    "borjeson2021": "Borjeson and Larsson-Edefors",
    "xie2023ma": "Xie and Zhao and Guan and Zhang and Ju",
    "ozbilgin2025": "Ozbilgin and Uysal",
    "nguyen2020": "Nguyen and Pham and Dang and Pham",
    # Batch B
    "yue2018": "Chaolei Yue and Jiawei Li and Jianfeng Sun and Ren Zhu and Xia Hou and Xiaoxi Zhang",
    "pech2025": "Sophonie Pech and Fabien Destic and Arnaud Dion and Angelique Rissons",
    "neves2024": "M. S. Neves and A. Lorences-Riesgo and C. M. Martins and S. Mumtaz and G. Charlet and P. Monteiro and F. P. Guiomar",
    "chen2025multisystem": "Xinyu Chen and Xia Hou and Shaowen Lu and Jiawei Li and Yongbo Fan and Jingyu Lv and Fan Fang and Xiaozhi Zhu and Zhenning Chang and Yingxia Huang and Jingyi Zhang and Yubing Li",
    "li2023status": "Ning Li",
    "guiomar2022coherent": "Fernando P. Guiomar and Marco A. Fernandes and Jose Leonardo Nascimento and Vitor A. Rodrigues and Paulo P. Monteiro",
    "sasaki2022leotracking": "Shane M. Walsh and Skevos F. E. Karpathakis and Ayden S. McCann and Benjamin P. Dix-Matthews and Alex M. Frost and David R. Gozzard and Sascha W. Schediwy",
    "wang2024fsoISL": "Guanhua Wang and Fang Yang and Jian Song and Zhu Han",
    "elamassie2023fso6g": "Mohammed Elamassie and Murat Uysal",
    "alhosani2025optical": "Asma Alhosani and Fatema AlShehhi and Mariam Almenhali and Hasan Abu Hilal",
    "stotts2021": "Larry B. Stotts and Larry C. Andrews",
    "correia2024": "Vitor D. Correia and Marco A. Fernandes and Paulo P. Monteiro and Fernando P. Guiomar and Goncalo M. Fernandes",
    "selim2026": "Hebat Allah O. Selim and Rania M. Abdallah and Moustafa H. Aly and Islam E. Shaalan",
    "zhou2024": "Huibin Zhou and Hao Song and Runzhou Zhang and Xinzhou Su and Kaiheng Zou and Yuxiang Duan and Narek Karapetyan and Haoqian Song and Zhe Zhao and Cong Liu and Kai Pang and Moshe Tur and Alan E. Willner",
    "ju2024": "Cheng Ju and Na Liu and Dongdong Wang and Danshi Wang and Jingze Yu and Yue Qiu",
    "li2019": "Yan Li and Mingwei Wu and Xinwei Du and Tianyu Song and Pooi-Yuen Kam",
    "xiang2018": "Qun Zhang and Yanfu Yang and Qian Xiang and Qianwen He and Zhongqing Zhou and Yong Yao",
    "xiang2015": "Meng Xiang and Songnian Fu and Ling Deng and Ming Tang and Perry Ping Shum and Deming Liu",
    "zheng2025fpga": "Tianqi Zheng and Kaihui Wang and Sheng Hu and Xiongwei Yang and Long Zhang and Chen Wang and Jianjun Yu",
    # Batch C
    "ge2026opll": "Biao Ge and Jincong Hu and Yaoping Wu and Ningyuan Zhong and Xihua Zou",
    "yang2024sat16qam": "Jin Yang and Xinquan Yang and Jingzhong Guo",
    "wang2025irs": "Jingyu Wang and Dingshan Gao and Ruzhao Chen",
    "stotts2023tutorial": "Larry B. Stotts and Larry C. Andrews",
    "elsayed2024ofdm": "Ebrahim E. Elsayed",
    "martins2021cpr": "Celestino S. Martins and Fernando P. Guiomar and Armando N. Pinto",
    "mosnier2025fso": "Marie-Bertille Mosnier and Sophonie Pech and Fabien Destic and Remi Douvenot and Helene Galiegue and Arnaud Dion and Angelique Rissons",
    "israel2023lcrd-early": "David J. Israel and Bernard L. Edwards and Richard L. Butler and John D. Moores and Sabino Piazzolla and Nic du Toit and Lena Braatz",
    "israel2024lcrd-char": "David J. Israel and Bernard L. Edwards and Richard L. Butler and John D. Moores and Sabino Piazzolla and Jonathan Woodward and Alan Hylton and Nic du Toit and Lena E. Braatz",
    "khatri2025illumat": "Farzana I. Khatri and Zachary Gonnsen and Jade P. Wang and Christian Rivera Rivera and Jamie Burnside and Richard L. Butler and Jessica Chang and Jean-pierre Chamoun and Benjamin Croop and Nicolas I. Cummings and Catherine E. DeVoe and Nicolaas du Toit and Jacob M. Gregory and Alan G. Hylton and Mahima Kaushik and Samuel S. Larson and Olga Mikulina and John D. Moores and Sabino Piazzolla and Patricia Randazzo and Thomas E. Roberts and Jennifer A. Sager and Suzanne E. Smith and Neal W. Spellmeyer and Kathy Strickler and Jeffrey D. Towns and John J. Veselka and Douglas T. Ward and James Torres and Jonathan R. Woodward and Miriam D. Wennersten and David J. Israel and Glenn B. Jackson and Bryan S. Robinson",
    "heine2023tesat": "Frank Heine and Andrej Brzoska and Mark Gregory and Thomas Hiemstra and Robert Mahn and Patricia Martin Pimentel and Herwig Zech",
    "lustica2025edrs-copernicus": "Alen Lustica and Sanja Samanovic and Domagoj Frank and Olga Bjelotomic Orsulic",
    "satoh2026lucas-operations": "Yohei Satoh and Takamasa Itahashi and Yutaka Takano and Shiro Yamakawa",
    "itahashi2025lucas-status": "Takamasa Itahashi and Yohei Satoh and Yutaka Takano and Shiro Yamakawa",
    "tarhouni2025fsoMesh": "Ferdaous Tarhouni and Ruibo Wang and Mohamed-Slim Alouini",
    "alimi2024revolutionizing": "Isiaka A. Alimi and Paulo P. Monteiro",
    "jain2025satelliteRFfso": "Varun Jain and B.V.R. Reddy and Ashish Payal",
    "valjus2025": "Carl Valjus and Raphael Wolf and Juraj Poliak",
}

# Additional citekey renames (wrong first author)
RENAMES = {
    "le2012dpll": "xie2012dpll",
    "sasaki2022leotracking": "walsh2022leotracking",
}


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    bib_text = BIB_PATH.read_text(encoding="utf-8")
    lit_text = LIT_PATH.read_text(encoding="utf-8") if LIT_PATH.exists() else ""

    author_applied = 0
    author_failed = 0
    rename_applied = 0

    # 1. Apply author updates
    for ck, authors_str in AUTHORS.items():
        pattern = rf"(@\w+\{{{ck},.*?author\s*=\s*\{{)([^}}]*)(\}})"
        match = re.search(pattern, bib_text, re.DOTALL)
        if match:
            old_author = match.group(2)
            new_text = bib_text[:match.start()] + match.group(1) + authors_str + match.group(3) + bib_text[match.end():]
            if new_text != bib_text:
                bib_text = new_text
                author_applied += 1
                print(f"  ✓ {ck}: '{old_author[:30]}...' → {len(authors_str.split(' and '))} authors")
            else:
                author_failed += 1
                print(f"  = {ck}: no change")
        else:
            author_failed += 1
            print(f"  ✗ {ck}: not found in bib")

    # 2. Apply citekey renames
    for old_ck, new_ck in RENAMES.items():
        old_marker = "{" + old_ck + ","
        new_marker = "{" + new_ck + ","
        if old_marker in bib_text:
            bib_text = bib_text.replace(old_marker, new_marker)
            lit_text = re.sub(rf'\b{old_ck}\b', new_ck, lit_text)
            rename_applied += 1
            print(f"  ✎ {old_ck} → {new_ck}")
        else:
            print(f"  ✗ {old_ck}: not found for rename")

    print(f"\nAuthors updated: {author_applied}, Failed: {author_failed}")
    print(f"Renames applied: {rename_applied}")

    if args.apply:
        BIB_PATH.write_text(bib_text, encoding="utf-8")
        if lit_text:
            LIT_PATH.write_text(lit_text, encoding="utf-8")
        print("Files written.")
    else:
        print("Dry run. Use --apply to write files.")


if __name__ == "__main__":
    main()
