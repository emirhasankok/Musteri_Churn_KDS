using Churn.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Churn.Controllers
{
    public class MusteriController : Controller
    {
        private readonly ChurnCrmDbContext _context;

        public MusteriController(ChurnCrmDbContext context)
        {
            _context = context;
        }

        public async Task<IActionResult> Index()
        {
            return View(await _context.Musterilers.ToListAsync());
        }

        public async Task<IActionResult> Details(int? id)
        {
            if (id == null) return NotFound();
            var musteri = await _context.Musterilers.FirstOrDefaultAsync(m => m.MusteriId == id);
            if (musteri == null) return NotFound();
            return View(musteri);
        }

        public async Task<IActionResult> Create()
        {
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Yas,KullanimSuresiAy,AylikHarcamaTl,DestekTalebiSayisi,SonGirisGunu,ChurnDurumu")] Musteriler musteri)
        {
            if (ModelState.IsValid)
            {
                // 1. Veritabanı tablosuna (Joker ile) erişiyoruz
                var tablo = _context.Set<Musteriler>();

                // 2. En yüksek ID'yi bulup 1 ekliyoruz
                var maxId = tablo.Any() ? tablo.Max(m => m.MusteriId) : 0;
                musteri.MusteriId = maxId + 1;

                // 3. Kaydetme işlemi
                _context.Add(musteri);
                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            return View(musteri);
        }

        public async Task<IActionResult> Edit(int? id)
        {
            if (id == null) return NotFound();
            var musteri = await _context.Musterilers.FindAsync(id);
            if (musteri == null) return NotFound();
            return View(musteri);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("MusteriId,Yas,KullanimSuresiAy,AylikHarcamaTl,DestekTalebiSayisi,SonGirisGunu,ChurnDurumu")] Musteriler musteri)
        {
            if (id != musteri.MusteriId) return NotFound();

            if (ModelState.IsValid)
            {
                try
                {
                    _context.Update(musteri);
                    await _context.SaveChangesAsync();
                }
                catch (DbUpdateConcurrencyException)
                {
                    if (!_context.Musterilers.Any(e => e.MusteriId == musteri.MusteriId))
                        return NotFound();
                    else
                        throw;
                }
                return RedirectToAction(nameof(Index));
            }
            return View(musteri);
        }

        public async Task<IActionResult> Delete(int? id)
        {
            if (id == null) return NotFound();
            var musteri = await _context.Musterilers.FirstOrDefaultAsync(m => m.MusteriId == id);
            if (musteri == null) return NotFound();
            return View(musteri);
        }

        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            var musteri = await _context.Musterilers.FindAsync(id);
            if (musteri != null)
            {
                _context.Musterilers.Remove(musteri);
                await _context.SaveChangesAsync();
            }
            return RedirectToAction(nameof(Index));
        }
    }
}
