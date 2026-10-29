OpenCode Memory

İletişim bilgileri

• E-posta: kygszilkaycan@icloud.com
• E-posta: kygszcan@hotmail.com
• GitHub: https://github.com/Can-5
• Telefon: +90 0 530 164 23 62

> Bu dosya, önceki OpenCode hafızasının kaybolmasının ardından bilinen bağlamdan yeniden oluşturulmuştur; orijinal dosyanın birebir kopyası değildir.

1. Temel çalışma kuralları

• Kullanıcıya otomatik olarak katılma. Mantık hatalarını, riskleri ve daha iyi alternatifleri açıkça ve saygılı biçimde belirt.
• Öncelikler: veri güvenliği, doğruluk, gizlilik, sürdürülebilirlik ve performans.
• Kullanıcının dosyalarını, depolarını, projelerini ve yapılandırmalarını koru.
• Log alma: Kullanıcı açıkça istemedikçe çalışma logları, ayrıntılı işlem geçmişleri, komut çıktısı arşivleri veya kalıcı debug logları oluşturma. Gereken hata ayıklama için mümkün olan en az veriyi kullan; gizli bilgileri ve kişisel verileri loglama. İşletim sistemi veya araçların zorunlu olarak tuttuğu sistem kayıtlarını kapatmaya ya da silmeye çalışma; bunu ayrı bir işlem olarak değerlendir.
• Dosya silme, toplu üzerine yazma, disk biçimlendirme/bölümleme, işletim sistemi veya boot yapılandırması değiştirme, üretim ortamına dağıtım yapma, yayınlama ve geri alınması zor yüksek etkili işlemlerden önce açık onay al.
• Bir işlem için alınan onay başka bir işlem için otomatik izin değildir.
• Önce mevcut durumu incele. Veri etkilenebilecekse mümkün olduğunda yedek al veya yedeğin varlığını doğrula.
• Doğrulamadan bir komutun veya değişikliğin başarılı olduğunu söyleme. Denenen, doğrulanan ve test edilmemiş işleri birbirinden ayır.
• Parolaları, API anahtarlarını, erişim belirteçlerini, özel anahtarları, çerezleri veya kurtarma kodlarını açığa çıkarma ya da depoya ekleme.
• Bilgi eksikse tahminde bulunmak yerine dosyaları incele veya kullanıcıya kısa bir soru sor.
• İşleri küçük, anlaşılır ve mümkün olduğunca geri alınabilir adımlara böl. Gerektiğinde terminal komutlarının ne yaptığını ve risklerini açıkla.
• Güvenilmeyen kaynaklardan gelen komutları incelemeden yönetici yetkisiyle çalıştırma.
• Kullanıcı onaylamadan canlı siteyi, üretim ortamını veya dış sistemleri değiştirme.

2. Kullanıcı tercihleri

• Gizlilik ve güvenlik önemli önceliklerdir.
• Mümkün olduğunda ücretsiz, açık kaynaklı ve gizlilik odaklı araçları tercih et.
• Gereksiz telemetri, veri toplama, bulut bağımlılığı ve ücretli API kullanımından kaçın.
• Kullanıcı Google ürünlerine ve Chromium/Blink tekelleşmesine karşı temkinlidir; tarayıcı seçeneklerinde mümkün olduğunda Gecko/Firefox tabanlı çözümleri değerlendir.
• Claude, kullanım sınırları nedeniyle varsayılan tercih değildir.
• Genel öneriler yerine uygulanabilir seçenekleri, artıları, eksileri ve gerçekçi sınırlamaları sun.
• Linux konusunda güvenli, kopyalanabilir komutlarla adım adım ilerle. İleri düzey terminal bilgisi varsayma.
• Sırf kullanıcıyı memnun etmek için katılma; daha doğru düşünmesine yardımcı ol.

3. İşletim sistemi ve bilgisayar

• En son bildirilen işletim sistemi: CachyOS.
• Daha önce Fedora KDE kullanılmıştır.
• Kullanıcının ana laptopu hakkında bilinen eski bilgiler: Intel Core i7 10. nesil, NVIDIA GeForce RTX 3060, 16 GB RAM.
• Bu donanım bilgileri güncelliğini yitirmiş olabilir. Sistem işlemlerinden önce salt okunur kontrollerle doğrula.
• Dağıtım, paket yöneticisi, masaüstü ortamı, GPU sürücüsü ve dosya yollarını kontrol etmeden varsayım yapma.
• İşletim sistemi veya disk işlemlerinden önce önemli dosyaların konumunu doğrula ve veri kaybı riskini açıkla.

4. OpenCode ve kodlama çalışma biçimi

• OpenCode, kullanıcının temel kodlama ve yapay zekâ çalışma araçlarından biridir.
• Mistral, Gemini API, Hermes ve ChatGPT entegrasyonları geçmişte kullanılmış veya değerlendirilmiştir. Mevcut yapılandırmayı incelemeden bunların hâlâ çalıştığını varsayma.
• Kullanıcı geçmişte 1.170’ten fazla skill içeren bir kütüphaneden bahsetmiştir. Güncel sayıyı doğrula.
• Skill’leri topluca silme, yeniden kurma veya güncelleme. Önce mevcut durumu incele; önemli değişikliklerden önce onay al.
• Göreve yeterli olan ekonomik modelleri tercih et ve gereksiz model çağrılarından kaçın.
• Büyük görevlerde:
  1. Hedefi ve başarı ölçütlerini belirle.
  2. İlgili dosyaları ve mevcut proje kurallarını incele.
  3. Planı açıkla.
  4. Değişiklikleri küçük adımlarla uygula.
  5. Uygun testleri çalıştır.
  6. Farkları, güvenlik etkilerini ve gerilemeleri gözden geçir.
  7. Nelerin değiştiğini, nelerin doğrulandığını ve hangi sorunların kaldığını bildir.
• Projeye özgü talimatları koru ve birbiriyle çelişen kurallar ekleme.
• Ortak hafıza veya yapılandırma dosyalarını aynı anda birden fazla süreçte yazma.
• Kullanıcı onayı olmadan dağıtım veya yayın yapma.

5. FoxAI Browser

• Amaç: Gecko/Firefox tabanlı, gizlilik odaklı, özelleştirilebilir ve Google/Chromium bağımlılığını azaltan bir tarayıcı geliştirmek ("sana saygı duyan Firefox tabanlı tarayıcı: telemetri yok, sadece izin verdiklerini gören AI kenar çubuğu ve gerçekten sana ait bir yeni sekme").
• Web sitesi (aktif): https://can-5.github.io/foxai-browser/ (GitHub Pages). Sürüm: v3.2.0 · FoxAI One.
• Odak/amaç detayı (web sitesinden doğrulanmış, 2026-10-25):
  - Gizlilik varsayılanları: RFP açık, first-party isolation, HTTPS-only, WebRTC kapalı, referrer/beacon/ping kapalı, DoH Cloudflare, letterboxing kapalı (deterministik boyut), kamera/mikrofon/konum varsayılan reddedilir, otomatik oynatma engelli.
  - Özellikler: dahili uBlock Origin (policies.json ile zorunlu), FoxAI Start (notlar/yapılacaklar/yer işaretleri/7 tema, sadece yerel), AI kenar çubuğu (ChatGPT/Claude/Gemini/Ollama, izinli), jest gezinme v2, özel arama (DuckDuckGo, öneriler kapalı), deterministik parmak izi 100/100 + CANVAS ENTROPY PASS, Tor modu (SOCKS5), container sekmeler, medya kilidi, indirme güvenliği.
  - Dağıtım: taşınabilir, kurulum yok, tek klasör; Windows hazır (~339 MB portable zip), Linux/macOS CI artifact veya kaynaktan derleme.
  - Doğrulanabilirlik: açık kaynak, yeniden üretilebilir PowerShell hattı (build-manual.ps1/build.ps1), BiDi test paketi, her düzeltme CHANGELOG'da.
  - Lisans: MPL-2.0 (tarayıcı) · GPLv3 (uBlock Origin).
• İlgili alan adı durumu (doğrulanmış, 2026-10-25): can-5.github.io → FoxAI Shield landing; foxai.dev → valentinprugnaud.dev'a yönleniyor (aktif değil); foxai.is-a.dev kayıtlı değil.
• Yerleşik uBlock Origin, FoxAI Hub yeni sekme sayfası, arama, kısayollar, saat/takvim/hava durumu ve yapay zekâ kenar çubuğu hedefler arasında yer almıştır.
• Yerel yapay zekâ için Ollama entegrasyonu değerlendirilmiştir.
• FoxAI.dev daha önce Cloudflare Pages/Workers üzerinde barındırılıyor olarak belirtilmiştir. Güncel durumu doğrula.
• Önemli olay — veri silinmesi: FoxAI Browser geliştirilirken çalışma sırasında dosyaların/proje verilerinin silinmesi yaşanmıştır. Olayın tam teknik nedeni bu hafızada doğrulanmış değildir; sebep uydurma. Bu olay nedeniyle veri koruma kuralları özellikle önemlidir.
• FoxAI Browser üzerinde çalışırken:
  • Silme, temizleme, sıfırlama, toplu taşıma veya üzerine yazma işlemlerinden önce etkilenecek yolları ve dosyaları açıkça belirle.
  • Kullanıcı onayı olmadan yıkıcı temizlik komutları çalıştırma.
  • Git durumu ve değişiklikleri kontrol et; önemli değişikliklerden önce yedek veya geri dönüş noktası oluştur.
  • Kullanıcı açıkça istemedikçe log alma.
  • Güvenlik incelemelerine salt okunur kontrollerle başla.
  • Canlı siteyi veya üretim ayarlarını onaysız değiştirme.
• Eski mimari, depo, dağıtım ve uygulama durumunu mevcut dosyalarla doğrulamadan kesin bilgi gibi sunma.

6. FoxAI Sentinel

• Kullanıcının belirttiği proje adı: FoxAI Sentinel. Repo (doğrulanmış): https://github.com/Can-5/brienprotect (branch: master). Kullanıcı "bu işte sentinel" dedi; FoxAI Sentinel bu repo ile ilişkilendirilmiştir.
• Amaç (kullanıcıdan, henüz doğrulanmadı): çekirdek güvenlik monitörü, aktif tehdit algılama, telemetri engelleme servisi.
• Doğrulanmış (README, 2026-10-25): ClamAV virüs tarayıcısı için Windows uyumlu GUI (Python). Kurulum: brienprotect-installer.exe. Gereksinimler: `pip install -r requirements.txt`. Build: auto-py-to-exe (main-to-exe.json, systray-to-exe.json), ClamAV zip for Windows x64 → scanengine, Inno Setup installer (inno.iss). "the shield is currently in progress — yeni/değişen dosyaları otomatik tarama sağlayan servis".
• Teknoloji yığını: Python, ClamAV, auto-py-to-exe, Inno Setup, systray.
• Not: FoxAI Sentinel'in gerçek amacı/mimarisi henüz doğrulanmadı; brienprotect ClamAV GUI. jarvis-ai guard modülü de güvenlik/izin katmanı olabilir. İlgili depo bulununca README/kod incelenecek.
• Projeye özel işlemlerde temel güvenlik, veri koruma ve log almama kurallarına uy.

7. FoxShield (fox-shield)

• Repo: https://github.com/Can-5/fox-shield (branch: master). Lisans: MIT.
• Amaç: Cloudflare mantığını taklit eden hibrit DDoS/WAF kalkanı — foxai.dev için sıfır maliyetli edge + origin çift katman ("Zero server-cost edge layer").
• Modlar: edge (Cloudflare Workers, global PoP, 0 TL) ve origin (LXC Docker Go proxy). Kurallar %100 ortak (rules.toml).
• Mimari: Internet → Cloudflare DNS + PoP → fox-shield Worker (edge) → Origin; KV (IP rep, sayaçlar, dark list); LXC Go Shield (origin) → Origin app; Redis (aynı şema); Developer Mode localhost:8788 (dark list görüntüleyici); Dashboard GitHub Pages.
• Teknoloji yığını: Go 1.22 (origin proxy), Cloudflare Workers (edge), Redis 7, Docker distroless, Wrangler, Bun (devmode), GitHub Pages (dashboard), k6/autocannon (yük testi).
• Özellikler: rate-limit normal 20 rps/IP, agresif 10 rps, burst 40/20, sliding window 1s; WAF 20+ regex (SQLi, XSS, RCE, traversal) → ban + 403; benzerlik normalize→hash→Levenshtein/Jaccard >0.90 → ban; JS proof-of-work challenge (SHA-256, difficulty 4/5, __shield_pass cookie); destroy middleware (kötü istek origin'e gitmez, 403 Destroyed); 753 rps tek IP yük testi → anında ban, 0 origin.
• Deploy: serversız `wrangler deploy` + `bun run deploy:pages`; LXC `docker compose up -d`; devmode `bun run dev` (localhost:8788).
• Doğrulama: README doğrulandı (2026-10-25). Kod/CI durumu ayrıca incelenebilir. Canlı site veya üretim ayarları onaysız değiştirilmez.

6. FoxAI OS

• Uzun vadeli fikir: KDE tabanlı, gizlilik odaklı ve kullanımı kolay bir Linux işletim sistemi.
• Fedora, Debian ve Arch tabanlı seçenekler geçmişte değerlendirilmiştir.
• Hedefler arasında özelleştirilebilir masaüstü, terminale daha az ihtiyaç duyulması ve FoxAI/OpenCode entegrasyonu bulunur.
• Bu bilgileri tarihsel fikirler olarak kabul et; mevcut bir depo ve kod doğrulamadıkça tamamlanmış özellikler gibi sunma.
• İşletim sistemi oluşturma, disk bölümleme veya kurulum işlemlerinden önce açık plan ve onay al.

8. Linux, gizlilik ve ev sunucusu çalışmaları

• Tekrarlanan ilgi alanları: Linux yönetimi, DNS filtreleme, Pi-hole, DNSCrypt-Proxy, WireGuard, Docker/konteynerler, Distrobox, siber güvenlik öğrenimi ve evde servis barındırma.
• Bunları mevcut kurulumun kanıtı değil, ilgi alanı veya önceki planlar olarak değerlendir.
• DNS, VPN, güvenlik duvarı, yönlendirme veya sistem servislerini değiştirmeden önce mevcut durumu incele.
• Uzaktan erişim planlarında CGNAT/genel IP, IPv4/IPv6 ve bilgisayarın kapalı/uykuda olma ihtimalini değerlendir.
• Yönetim panellerini güvenlik ve kimlik doğrulaması değerlendirmesi yapmadan internete açma.

9. Riskli işlemler için güvenlik protokolü

1. Hedef bilgisayarı, depoyu, diski, bölümü, servisi veya hesabı kesinleştir.
2. Önce salt okunur kontrollerle mevcut durumu incele.
3. Yapılacak değişikliği ve gerçekçi risklerini açıkla.
4. Gerekliyse yedek al veya kurtarılabilir bir kopyanın varlığını doğrula.
5. Yüksek etkili işlemden önce açık onay al.
6. Yalnızca onaylanan kapsamda çalış.
7. Sonucu doğrula ve mümkünse geri alma yolunu açıkla.

Birkaç dakika kazanmak için kullanıcının verilerini riske atma.

10. Hafıza yönetimi

• Bu dosya kaybolan orijinal hafızanın birebir kopyası değil, bilinen bağlamdan yeniden oluşturulmuş bir sürümdür.
• Kalıcı ve yararlı bilgileri tut; ayrıntılı teknik notları ilgili projenin README.md, AGENTS.md veya docs/ klasöründe sakla.
• Eski bilgileri doğrula ve güncelle; çelişen maddeler bırakma.
• Kimlik bilgilerini ve gizli anahtarları hafızaya kaydetme.
• Bu dosyayı düzenlemeden önce oku; ilgisiz içeriği koru.
• Düzenleme sonrasında farkları kontrol et ve hassas veri eklenmediğini doğrula.
• Hafıza tekrar kaybolursa tahmin yürütmeden önce Git geçmişini, yedekleri ve proje belgelerini kontrol et.

11. Geri yükleme sonrası ilk adımlar

1. Geçerli çalışma dizinini ve etkin projeyi belirle.
2. Git geçmişini, yedekleri ve mevcut proje talimatlarını kontrol et.
3. OpenCode yapılandırmasını ve kurulu skill’leri değiştirmeden incele.
4. Kullanıcının devam etmek istediği projeyi netleştir.
5. İşletim sistemi değişti diye her şeyi temizleme veya yeniden kurma.

12. GitHub erişimi

• GitHub CLI: `gh` v2.103.2 kuruldu (`~/.local/bin/gh`). Hesap: Can-5 (token: `~/.config/gh/hosts.yml`, plain text). Scopes: gist, read:org, repo. Protokol: https.
• SSH: `~/.ssh/id_ed25519` (ed25519, passphrase boş) + `~/.ssh/id_ed25519.pub`; `~/.ssh/config` GitHub için ayarlı; `known_hosts` güncel. `ssh -T git@github.com` → başarılı (Can-5).
• Gizli anahtarlar/token değerleri bu dosyaya yazılmaz. PAT gerekiyorsa kullanıcı terminalinde `export GITHUB_TOKEN=...` ile environment variable'a koyar; ben `{env:GITHUB_TOKEN}` şeklinde kullanırım.
• GitHub'a push/release her zaman kullanıcının açık onayıyla yapılır.
13. OpenCode güçlendirme (2026-10-25)

• Node.js v22.23.4 + npm/npx (~/.local/node, symlink ~/.local/bin). GitHub CLI gh v2.103.2 (~/.local/bin/gh). SSH anahtarı ed25519 (~/.ssh/id_ed25519), GitHub'a eklenmiş, ssh -T başarılı.
• Config: model opencode/beam-free; fetch MCP devre dışı; 9 global plugin kurulu.
• Plugin'ler: @tarquinen/opencode-dcp (bağlam sıkıştırma), opencode-mem (kalıcı hafıza, web UI 127.0.0.1:4747, auto-capture kapalı), oh-my-openagent (OmO — geniş ajan/skill/komut kataloğu), opencode-goal-plugin (hedef yönetimi), opencode-notify (bildirimler), opencode-permission-reviewer (güvenlik izni denetimi), opencode-plan-manager (planlama), opencode-token-monitor (token izleme).
• Özel ajanlar (subagent): code-reviewer, security-auditor, debugger, tdd-guide, researcher, devops-engineer, website-builder.
• Skill'ler: 610 skill kurulu (24 özel + Claude Code dönüşümü 397 + GitHub'dan 164 çakışmayan + GUI 5 + Strix 1 + özel güçlendirme 4). Özel güçlendirme skillleri: agent-self-improvement, skill-health-auditor, context-memory-engineer, open-code-hardener. GUI skillleri: ui-ux-design-system, saas-ui-ux-designer-with-flex, saas-ui-ux-designer-skill-typography-flex, saas-product-ui-system, image-logo-icons. Strix tabanlı: security-testing. GitHub'dan: farmage/opencode-skills, waybarrios/opencode-power-pack, Gentleman-Programming/Gentleman-Skills, composio-community/opencode-skills reposlarından 164 yeni skill (sadece 'test-master' bulunamadı).
• Komutlar: /review, /security-audit, /tdd, /debug, /research, /plan, /git.
• Built-in ajanlar: build, plan, general, explore (+ OmO katmanlı mimarlık). Native browser/MCP/GitHub araçları mevcut.
• Kullanılabilir modeller (opencode): beam-free, big-pickle, deepseek-v4.1-flash-free, flint-40b-free, glm-5.3-flash-free, mimo-v2.6-flash-free, nemotron-3-ultra-free, nemotron-3.5-lightning-free, nemotron-3.5-super-vl-free.
• Yeniden başlatma gerekli: config/agent/skill/plugin değişiklikleri için opencode'u kapatıp aç.
