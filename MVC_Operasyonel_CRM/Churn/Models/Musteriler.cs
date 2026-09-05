using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Churn.Models;

public partial class Musteriler
{
    [Key]
    [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
    public int MusteriId { get; set; }

    public int Yas { get; set; }

    public int KullanimSuresiAy { get; set; }

    public decimal AylikHarcamaTl { get; set; }

    public int? DestekTalebiSayisi { get; set; }

    public int SonGirisGunu { get; set; }

    public bool? ChurnDurumu { get; set; }
}
